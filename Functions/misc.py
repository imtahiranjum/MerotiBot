import random
from art import text2art


def text_converter_random(text):
    return str(text2art(text, random.choice(list)))


def text_converter(text, font):
    return text2art(text, font)


fonts = "*************----**************\n"
counter = 0


def list_fonts():
    for x in list:
        global counter
        counter = counter + 1
        global fonts
        fonts += f"{counter}. {x} \n"
    return fonts
