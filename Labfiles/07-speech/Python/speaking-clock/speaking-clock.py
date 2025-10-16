from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
import azure.cognitiveservices.speech as speech_sdk

def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        global speech_config

        # Get config settings
        load_dotenv()
        speech_key = os.getenv('SPEECH_KEY')
        speech_region = os.getenv('SPEECH_REGION')

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
        print('Ready to use speech service in:', speech_config.region)

        # Get spoken input
        command = TranscribeCommand()
        if command.lower() == 'what time is it?':
            TellTime()

    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''

    # Configure speech recognition
    current_dir = os.getcwd()
    audioFile = current_dir + '/time.wav'
    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)


    # Process speech input
    print("Listening...")
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)


    # Return the command
    return command


def TellTime():
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)


    # Configure speech synthesis
    output_file = "output.wav"
    speech_config.speech_synthesis_voice_name = "tr-TR-EmelNeural"
    audio_config = speech_sdk.audio.AudioConfig(filename=output_file)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)


    # Synthesize spoken output
    responseSsml = " \
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
        <voice name='tr-TR-EmelNeural'> \
            {} \
            <break strength='weak'/> \
            Time to end this lab! \
        </voice> \
    </speak>".format(response_text)
    speak = speech_synthesizer.speak_ssml_async(responseSsml).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
    else:
        print("Spoken output saved in " + output_file)


if __name__ == "__main__":
    main()