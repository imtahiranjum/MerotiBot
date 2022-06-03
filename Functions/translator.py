import uuid
import os
import requests
import discord
from _datetime import datetime
from webscrap import quote_scraped, taymiyah_quote_scraped,\
    ghazaali_quote_scraped, al_jawzi_quote_scraped, quote_scraped_islamic

subscription_key = f"{os.environ['microsoft_translator_api_token']}"


def microsoft_translator(text_to_translate, to_language, ctx):
    language_correct = to_language.lower()
    if language_correct == "urdu":
        language_correct = "ur"
    elif language_correct == "arabic":
        language_correct = "ar"
    elif language_correct == "english":
        language_correct = "en"
    elif language_correct == "chinese":
        language_correct = "zh"
    elif language_correct == "russian":
        language_correct = "ru"
    elif language_correct == "japanese":
        language_correct = "ja"
    elif language_correct == "hindi":
        language_correct = "hi"
    elif language_correct == "turkish":
        language_correct = "tr"
    elif language_correct == "tamil":
        language_correct = "ta"
    elif language_correct == "punjabi":
        language_correct = "pa"
    elif language_correct == "arabic":
        language_correct = "ar"
    elif language_correct == "german":
        language_correct = "de"
    elif language_correct == "spanish":
        language_correct = "es"
    else:
        language_correct = f"{to_language}"

    dictionary_for_naming = {"ur": "Urdu", "en": "English",
                             "zh": "Chinese", "ar": "Arabic",
                             "pa": "Punjabi", "hi": "Hindi",
                             "tr": "Turkish", "pr": "Persian"}

    str(text_to_translate)
    endpoint = "https://api.cognitive.microsofttranslator.com"
    location = "southeastasia"
    path = '/translate'
    params = {
        'api-version': '3.0',
        'to': [language_correct]
    }
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': f'{text_to_translate}'
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.text
    response = response.replace('[', "").replace(",", "").replace("{", "").replace(":", "").replace("}", "").replace(
        "]", "")
    split_response = response.split('""')
    last_item = split_response[-1].replace('"', "")
    list_of = split_response[0:-1]
    list_of.append(last_item)
    formatted_translation = f"Detected Language: *{dictionary_for_naming.get(list_of[2])}*\nText: *{text_to_translate}*\n" \
                            f"Translated to: {dictionary_for_naming.get(list_of[-1])}\nTranslation:- \n**{list_of[5]}**"

    embed = discord.Embed(title="Translation Card", color=0x91e609, timestamp=datetime.utcnow())
    embed.add_field(name="Detected language: ", value=f"{dictionary_for_naming.get(list_of[2])}", inline=False)
    embed.add_field(name="Text: ", value=f"{text_to_translate}", inline=False)
    embed.add_field(name="Translated to: ", value=f"{dictionary_for_naming.get(list_of[-1])}", inline=False)
    embed.add_field(name="Translation:- ", value=f"```fix\n{list_of[5]}```", inline=False)
    embed.set_footer(text=f"✔ Request by: {ctx.author.name}")
    if len(list_of[5]) <= 1024:
        return embed
    else:
        return formatted_translation


def microsoft_translator_ur(text_to_translate, ctx):
    dictionary_for_naming = {"ur": "Urdu", "en": "English",
                             "zh": "Chinese", "ar": "Arabic",
                             "pa": "Punjabi", "hi": "Hindi",
                             "tr": "Turkish"}
    str(text_to_translate)
    endpoint = "https://api.cognitive.microsofttranslator.com"
    location = "southeastasia"
    path = '/translate'
    params = {
        'api-version': '3.0',
        'to': ['ur']
    }
    constructed_url = endpoint + path
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': f'{text_to_translate}'
    }]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.text
    response = response.replace('[', "").replace(",", "").replace("{", "").replace(":", "").replace("}", "").replace(
        "]", "")
    split_response = response.split('""')
    last_item = split_response[-1].replace('"', "")
    list_of = split_response[0:-1]
    list_of.append(last_item)
    translated_text = list_of[5]
    if "Quote:-" in text_to_translate:
        translated_text.split('"')
        print(translated_text[0].replace("`", "").replace("n", "").replace("-", ""))
        print(translated_text[-1])

    formatted_translation = f"Detected Language: *{dictionary_for_naming.get(list_of[2])}*\nText: *{text_to_translate}*\n" \
                            f"Translated to: Urdu\nTranslation:- \n**{list_of[5]}**"
    embed = discord.Embed(title="Translation Card", color=0x91e609, timestamp=datetime.utcnow())
    embed.add_field(name="Detected language: ", value=f"{dictionary_for_naming.get(list_of[2])}", inline=False)
    embed.add_field(name="Text: ", value=f"{text_to_translate}", inline=False)
    embed.add_field(name="Translated to: ", value=f"{dictionary_for_naming.get(list_of[-1])}", inline=False)
    embed.add_field(name="Translation:- ", value=f"```fix\n{list_of[5]}```", inline=False)
    embed.set_footer(text=f"✔ Request by: {ctx.author.name}")
    if len(list_of[5]) <= 1024:
        return embed
    else:
        return formatted_translation


def microsoft_translator_quote_ur(ctx, quote_of):
    if quote_of == "g":
        to_translate = ghazaali_quote_scraped()
    elif quote_of == "t":
        to_translate = taymiyah_quote_scraped()
    elif quote_of == "j":
        to_translate = al_jawzi_quote_scraped()
    elif quote_of == "i":
        to_translate = quote_scraped_islamic()
    elif quote_of == "q":
        to_translate = quote_scraped()
    else:
        to_translate = quote_scraped()

    str(to_translate)
    quote = to_translate.split('“')
    quote = quote[1]
    quote = quote.split("”")
    quote = quote[0]
    text_to_translate = quote
    quote_to_show = to_translate

    dictionary_for_naming = {"ur": "Urdu", "en": "English",
                             "zh": "Chinese", "ar": "Arabic",
                             "pa": "Punjabi", "hi": "Hindi",
                             "tr": "Turkish"}
    str(text_to_translate)
    endpoint = "https://api.cognitive.microsofttranslator.com"
    location = "southeastasia"
    path = '/translate'
    params = {
        'api-version': '3.0',
        'to': ['ur']
    }
    constructed_url = endpoint + path
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': f'{text_to_translate}'
    }]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.text
    response = response.replace('[', "").replace(",", "").replace("{", "").replace(":", "").replace("}", "").replace(
        "]", "")
    split_response = response.split('""')
    last_item = split_response[-1].replace('"', "")
    list_of = split_response[0:-1]
    list_of.append(last_item)

    formatted_translation = f"Detected Language: *{dictionary_for_naming.get(list_of[2])}*\n*{text_to_translate}*\n" \
                            f"Translated to: Urdu\nTranslated Quote:- \n**{list_of[5]}**"
    embed = discord.Embed(title="Quote with Translation", color=0x91e609, timestamp=datetime.utcnow())
    embed.add_field(name="Detected language: ", value=f"{dictionary_for_naming.get(list_of[2])}", inline=False)
    embed.add_field(name="Text: ", value=f"{quote_to_show}", inline=False)
    embed.add_field(name="Translated to: ", value=f"{dictionary_for_naming.get(list_of[-1])}", inline=False)
    embed.add_field(name="Translated Quote:- ", value=f"```fix\n{list_of[5]}```", inline=False)
    try:
        if ctx == "none":
            embed.set_footer(text=f"✔ Requested Autonomously")
        else:
            embed.set_footer(text=f"✔ Request by: {ctx.author.name}")
    except:
        embed.set_footer(text=f"✔ Requested Autonomously")

    if len(list_of[5]) <= 1024:
        return embed
    else:
        return formatted_translation