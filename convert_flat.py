import json
import re

from services.writer import Writer

with open('answers.json') as json_file:
    answers = json.load(json_file)['answers']

result = []

category = {
    'tema1_platser-tycker-om-dagtid': 4,
    'tema1_platser-tycker-om-kvälls-nattetid': 6,
    'tema1_platser-tycker-inte-om-dagtid': 5,
    'tema1_platser-tycker-inte-om-kvälls-nattetid': 7,
    'tema1_mer-boende': 8,
    'tema1_mer-mötesplatser': 10,
    'tema1_mer-service': 9,
    'tema1_mer-natur': 11,
    'tema1_mer-annat': 12
}

place_types_0 = [
    'tema1_platser-tycker-om-dagtid',
    'tema1_platser-tycker-om-kvälls-nattetid',
    'tema1_platser-tycker-inte-om-dagtid',
    'tema1_platser-tycker-inte-om-kvälls-nattetid'
]

place_types_2 = [
    'tema1_mer-boende', 'tema1_mer-mötesplatser', 'tema1_mer-service',
    'tema1_mer-natur', 'tema1_mer-annat'
]

template_0 = {
    'tema1_platser-tycker-om-dagtid':
    "<b>Varför tycker du om platsen? Vad gör du där?</b><ul>{}</ul>",
    'tema1_platser-tycker-om-kvälls-nattetid':
    '<b>Varför tycker du om platsen?</b><ul>{}</ul>',
    'tema1_platser-tycker-inte-om-dagtid':
    '<b>Varför tycker du INTE om platsen?</b><ul>{}</ul>',
    'tema1_platser-tycker-inte-om-kvälls-nattetid':
    '<b>Varför tycker du INTE om platsen?</b><ul>{}</ul>',
    'tema1_mer-boende': '<b>Vilken upplåtelseform vill du ha?</b><ul>{}</ul>',
    'tema1_mer-mötesplatser':
    '<b>Vilken typ av Mötesplats och socialt liv behövs här?</b><ul>{}</ul>',
    'tema1_mer-service': '<b>Vilken typ av Service?</b><ul>{}</ul>',
    'tema1_mer-natur':
    '<b>Vilken typ av Natur, odlingar och grönska behövs?</b><br><br>{}<br><br>',
    'tema1_mer-annat': '<b>Vad är det som behövs?</b><br><br>{}<br><br>'
}

template_1 = {
    'tema1_platser-tycker-om-dagtid':
    "<b>Varför tycker du om platsen? Vad gör du där?</b><ul><li>Det finns mycket att göra där, till exempel: {}</li></ul>",
    'tema1_platser-tycker-om-kvälls-nattetid':
    "<b>Varför tycker du om platsen?</b><ul><li>Annat: {}</li></ul>",
    'tema1_platser-tycker-inte-om-dagtid':
    "<b>Varför tycker du INTE om platsen?</b><ul><li>Annat: {}</li></ul>",
    'tema1_platser-tycker-inte-om-kvälls-nattetid':
    "<b>Varför tycker du INTE om platsen?</b><ul><li>Annat: {}</li></ul>",
    'tema1_mer-boende': '<b>Vilken typ av hus behövs?</b><ul>{}</ul>',
    'tema1_mer-mötesplatser':
    '<b>Vilken typ av Mötesplats och socialt liv behövs här?</b><ul><li>Annat: {}</li></ul>',
    'tema1_mer-service': "<ul><li>Annan service: {}</li></ul>",
    'tema1_mer-natur':
    '<b>Varför vill du ha mer Natur, odlingar och grönska här?</b><br><br>{}<br><br>',
    'tema1_mer-annat': '<b>Varför vill du ha detta här?</b><br><br>{}<br><br>'
}

template_2 = {
    'tema1_platser-tycker-om-dagtid':
    '<b>Varför tycker du om platsen? Vad gör du där?</b><ul><li>Annat: {}</li></ul>',
    'tema1_platser-tycker-om-kvälls-nattetid':
    '',
    'tema1_platser-tycker-inte-om-dagtid':
    '',
    'tema1_platser-tycker-inte-om-kvälls-nattetid':
    '',
    'tema1_mer-boende':
    '<b>Varför vill du ha byggnader här?</b><br><br>{}<br><br>',
    'tema1_mer-mötesplatser':
    '<b>Varför vill du ha Mötesplats och socialt liv här?</b><br><br>{}<br><br>',
    'tema1_mer-service':
    '<b>Varför vill du ha service här?</b><br><br>{}<br><br>',
    'tema1_mer-natur':
    '<b>Vad är bra med den här platsen, vad ska man spara?</b><br><br>{}<br><br>',
    'tema1_mer-annat':
    '<b>Vad är bra med den här platsen, vad ska man spara?</b><br><br>{}<br><br>'
}

template_3 = {
    'tema1_platser-tycker-om-dagtid':
    '',
    'tema1_platser-tycker-om-kvälls-nattetid':
    '',
    'tema1_platser-tycker-inte-om-dagtid':
    '',
    'tema1_platser-tycker-inte-om-kvälls-nattetid':
    '',
    'tema1_mer-boende':
    '<b>Vad är bra med den här platsen, vad ska man spara?</b><br><br>{}<br><br>',
    'tema1_mer-mötesplatser':
    '<b>Vad är bra med den här platsen, vad ska man spara?</b><br><br>{}<br><br>',
    'tema1_mer-service':
    '<b>Vad är bra med den här platsen, vad ska man spara? </b><br><br>{}<br><br>',
    'tema1_mer-natur':
    '<b>Vad är dåligt med den här platsen, vad måste man göra bättre?</b><br><br>{}<br><br>',
    'tema1_mer-annat':
    '<b>Vad är dåligt med den här platsen, vad måste man göra bättre?</b><br><br>{}<br><br>'
}

template_4 = {
    'tema1_platser-tycker-om-dagtid': '',
    'tema1_platser-tycker-om-kvälls-nattetid': '',
    'tema1_platser-tycker-inte-om-dagtid': '',
    'tema1_platser-tycker-inte-om-kvälls-nattetid': '',
    'tema1_mer-boende':
    '<b>Vad är dåligt med den här platsen, vad måste man göra bättre?</b><br><br>{}<br><br>',
    'tema1_mer-mötesplatser':
    '<b>Vad är dåligt med den här platsen, vad måste man göra bättre?</b><br><br>{}<br><br>',
    'tema1_mer-service':
    '<b>Vad är dåligt med den här platsen, vad måste man göra bättre?</b><br><br>{}<br><br>',
    'tema1_mer-natur': '',
    'tema1_mer-annat': '',
}

templates = [template_0, template_1, template_2, template_3, template_4]


def convert_place(place):
    return {
        'lat': place['lat'],
        'lng': place['lng'],
        'title/en': text.split('\n')[0],
        'body/en': text
    }


def convert_type(place_type, data):
    places = data[place_type]

    converted_places = []

    for place in places:
        converted_place = convert_place(place_type, place)
        if converted_place:
            converted_places.append(convert_place(place_type, place))

    return converted_places


def convert_answer(answer):
    print('answer: ' + str(answer['id']))

    if not 'tyck till' in answer:
        return {}

    tema1_0 = answer['tyck till']['tema1_0']
    tema1_2 = answer['tyck till']['tema1_2']

    converted_answer = {}

    for place_type in place_types_0 + place_types_2:
        if place_type in tema1_0:
            converted_answer[place_type] = convert_type(place_type, tema1_0)
        elif place_type in tema1_2:
            converted_answer[place_type] = convert_type(place_type, tema1_2)
        else:
            continue

    return converted_answer


final_list = {}

for place_type in place_types_0 + place_types_2:
    final_list[place_type] = []

    for answer in answers:
        converted_answer = convert_answer(answer)

        if converted_answer.get(place_type):
            final_list[place_type].extend(converted_answer[place_type])

    Writer.write_json(final_list[place_type], '{}.json'.format(place_type))

#Writer.write_csv(gillar_dagtid, 'places.csv')
