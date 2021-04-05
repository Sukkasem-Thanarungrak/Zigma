# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
# This code has been adapted from the example (https://github.com/Azure-Samples/cognitive-services-speech-sdk)

import azure.cognitiveservices.speech as speechsdk
import re

def speech_recognize():
    print("Say something like - \"I bought a coffee for 5 dollars\" or \"coffee, 5 dollars\"")
    print("USE CURRENCY AS DOLLARS ONLY!!")
    print(">>>")

    """performs one-shot intent recognition from input from the default microphone"""


    # Set up the config for the intent recognizer (remember that this uses the Language Understanding key, not the Speech Services key)!

    """
    speech_config = speechsdk.SpeechConfig(
        subscription="a0b05e25adb746ae9df5160209778f54",
        region="southeastasia")

    # Automatic language detection - ทำให้ผู้ใช้สามารถเลือกที่จะอัดเป็นภาษาไทยหรืออังกฤษก็ได้ (สามารถแยกได้มากสุดถึง 4 ภาษา)
    auto_detect_source_language_config = \
            speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "th-TH"])

    speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, 
            auto_detect_source_language_config=auto_detect_source_language_config, )
    """

    # Set up the config for the intent recognizer (remember that this uses the Language Understanding key, not the Speech Services key)!
    intent_config = speechsdk.SpeechConfig(
        subscription="dc8e5eadc85f45dfb7b3fe43216e907a",
        region="australiaeast")

    # Set up the intent recognizer
    intent_recognizer = speechsdk.intent.IntentRecognizer(speech_config=intent_config)

    # set up the intents that are to be recognized. These can be a mix of simple phrases and
    # intents specified through a LanguageUnderstanding Model.

    model = speechsdk.intent.LanguageUnderstandingModel(app_id="23c319e7-f4a9-4cd6-b928-ce1a8ea43fa2")
    intents = [
        (model, "Food"),
        ("This is a test.", "test"),
        ("Switch to channel 34.", "34"),
        ("what's the weather like", "weather"),
    ]
    intent_recognizer.add_intents(intents)
    global intent_result
    intent_result = intent_recognizer.recognize_once()
    auto_detect_source_language_result = speechsdk.AutoDetectSourceLanguageResult(intent_result)
    detected_language = auto_detect_source_language_result.language

    # Check the results
    if intent_result.reason == speechsdk.ResultReason.RecognizedIntent:
        print("Recognized: \"{}\" with intent id `{}`".format(intent_result.text, intent_result.intent_id))
        text_seperater()
    elif intent_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(intent_result.text))
        text_seperater()
    elif intent_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(intent_result.no_match_details))
    elif intent_result.reason == speechsdk.ResultReason.Canceled:
        print("Intent recognition canceled: {}".format(intent_result.cancellation_details.reason))
        if intent_result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(intent_result.cancellation_details.error_details))
    

# create lists contains items in different category
beverages = ["cola", "water", "juice", "smoothie", "milk", "drink"]
food = ["omelette", "rice", "egg", "steak", "fried", "pork", "beef"]
clothing = ["shirt", "shorts", "pants", "sweater", "jeans"]
etc = []


def category_create():
    global category
    category = "Unknown"

    # Create a list from recognized text
    seperated_list = intent_result.text.split()

    # Find a keyword to match a category
    for i in range(len(seperated_list)):
        if seperated_list[i-1] in beverages:
            category = "Beverages"
            break
        elif seperated_list[i-1] in food:
            category = "Food"
            break
        elif seperated_list[i-1] in clothing:
            category = "Clothing"
            break
        elif seperated_list[i-1] in etc:
            category = "etc."
            break
    
    # In case the program can't match any category
    if category == "Unknown":
        while category == "Unknown":
            print("We can't find your item in our database")
            item = input("What's your item: ").lower()
            print("Choose a category\n[Beverages] [Food] [Clothing] [etc]")
            user_input = input(">>>").lower()
            if user_input == "beverages":
                category = "Beverages"
                beverages.append(item)
            elif user_input == "food":
                category = "Food"
                food.append(item)
            elif user_input == "clothing":
                category = "Clothing"
                clothing.append(item)
            elif user_input == "etc":
                category = "etc."
                etc.append(item)
            else:
                category = "Unknown"
                print("Please try again.")


# This function will seperate the product you bought from the price
def text_seperater():

    ini_string = intent_result.text

    # find letter
    activity = " ".join(re.split("[^a-zA-Z]+", ini_string))

    # find number
    price = "".join(re.split("[^0-9$]+", ini_string))

    category_create()

    # Conclusion
    print("Activity: ", str(activity))
    print("Price: ", str(price))
    print("Category: ", category)
    print()

    # Run the program again
    speech_recognize()
    

speech_recognize()

# Remain silent if you want to exit the program