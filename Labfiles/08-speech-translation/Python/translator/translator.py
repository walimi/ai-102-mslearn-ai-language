from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config
        global translation_config

        # Get Configuration Settings
        load_dotenv()
        speech_key = os.getenv('KEY')
        speech_region = os.getenv('REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(speech_key, speech_region)
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language('tr')
        translation_config.add_target_language('fa')
        translation_config.add_target_language('uz')
        translation_config.add_target_language('de')
        translation_config.add_target_language('ur')
        print('Ready to translate from ', translation_config.speech_recognition_language)
        

        # Configure speech
        speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
        print('Ready to use speech service in: ', speech_config.region)

        # Get user input
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input('\nEnter a target language\n tr = Turkish\n fa = Iranian\n uz = Uzbeki\n ur = Urdu \nEnter anything else to stop\n').lower()
            if targetLanguage in translation_config.target_languages:
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'
                

    except Exception as ex:
        print(ex)

def Translate(targetLanguage):
    translation = ''

    # Translate speech
    audio_config_in = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config_in)
    print("Speak into your microphone.")
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations[targetLanguage]
    print(translation)


    # Synthesize translation
    voices = {
        "tr": "tr-TR-EmelNeural",
        "fa": "fa-IR-FaridNeural",
        "uz": "uz-UZ-SardorNeural",
        "ur": "ur-PK-AsadNeural"
    }

    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    audio_config_out = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config_out)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)


if __name__ == "__main__":
    main()
