﻿using System;
using System.IO;
using System.Text;
using Microsoft.Extensions.Configuration;

// Import namespaces
using Azure;
using Azure.AI.TextAnalytics;

namespace text_analysis
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string aiSvcEndpoint = configuration["AIServicesEndpoint"];
                string aiSvcKey = configuration["AIServicesKey"];

                // Create client using endpoint and key
                AzureKeyCredential credentials = new AzureKeyCredential(aiSvcKey);
                Uri endpoint = new Uri(aiSvcEndpoint);
                TextAnalyticsClient aiClient = new TextAnalyticsClient(endpoint, credentials);


                // Analyze each text file in the reviews folder
                var folderPath = Path.GetFullPath("./reviews");  
                DirectoryInfo folder = new DirectoryInfo(folderPath);
                foreach (var file in folder.GetFiles("*.txt"))
                {
                    // Read the file contents
                    Console.WriteLine("\n-------------\n" + file.Name);
                    StreamReader sr = file.OpenText();
                    var text = sr.ReadToEnd();
                    sr.Close();
                    Console.WriteLine("\n" + text);

                    // Get language
                    DetectedLanguage detectedLanguage = aiClient.DetectLanguage(text); 
                    Console.WriteLine($"\nLanguage: {detectedLanguage.Name}");


                    // Get sentiment
                    DocumentSentiment sentimentAnalysis = aiClient.AnalyzeSentiment(text);
                    Console.WriteLine($"\nSentiment: {sentimentAnalysis.Sentiment}");

                    // Get key phrases


                    // Get entities


                    // Get linked entities


                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }



    }
}
