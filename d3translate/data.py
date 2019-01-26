'''Translation data and config'''
# pylint: disable=C0103,C0326

from pathlib import Path


# process paths
basepath = Path(__file__).parent.parent

inputpath: Path = basepath.joinpath('input')
textpath = inputpath.joinpath('msg/engus')
soundpath = inputpath.joinpath('sound')

buildpath: Path = basepath.joinpath('build')

outputpath: Path = basepath.joinpath('output')
credentialspath: Path = basepath.joinpath('google.credentials.json')


# internals
ignoretext = [
    '(dummyText)',
    '%null%',
    ' ',
    '',
]
ignoretext_infix = [
    '<',
    '%',
    '*'
]
ignorefiles_prefix = [
    'メニュー共通テキスト',
    'テキスト表示用タグ一覧',
    'FDP_システムメッセージ',
    'FDP_キーガイド',
    'FDP_NGWord'
]
voicefiles_prefix = [
    '会話',
    'ムービー字幕'
]


# times the translation is run through random languages
translate_steps = 5

voice_sample_excludes = {
    # horace / gael sample name overlaps... why
    'v051000000':  ['fdp_vm35', 'fdp_vm33', 'fdp_vm38', 'fdp_vm40'],
    'v051000000b': ['fdp_vm35', 'fdp_vm33', 'fdp_vm38', 'fdp_vm40'],
    'v051000100':  ['fdp_vm35', 'fdp_vm33', 'fdp_vm38', 'fdp_vm40'],
    'v051000100b': ['fdp_vm35', 'fdp_vm33', 'fdp_vm38', 'fdp_vm40'],
    'v051001000':  ['fdp_vm35', 'fdp_vm33', 'fdp_vm38', 'fdp_vm40'],
    'v051001000b': ['fdp_vm35', 'fdp_vm33', 'fdp_vm38', 'fdp_vm40'],
    'v051002000':  ['fdp_vm35', 'fdp_vm33', 'fdp_vm38', 'fdp_vm40'],
    'v051002000b': ['fdp_vm35', 'fdp_vm33', 'fdp_vm38', 'fdp_vm40'],
    'v051003000':  ['fdp_vm35', 'fdp_vm33', 'fdp_vm38', 'fdp_vm40']
}

# character voice designations
# !ADJUST depending on installed or preferred voices
voicefilter = ['english', 'ivona']
voices = [
    {'name': 'DEFAULT', 'type': 'acapellabox', 'voice': 'WillHappy',
        'lower': 0, 'upper': 0, },

    {'name': 'oceiros', 'type': 'acapellabox', 'voice': 'WillLittleCreature',
        'lower': 500, 'upper': 503, },
    {'name': 'oceiros', 'type': 'acapellabox', 'voice': 'WillLittleCreature',
        'lower': 24000000, 'upper': 24100000, },

    {'name': 'price', 'type': 'acapellabox', 'voice': 'WillFromAfar',
        'lower': 600, 'upper': 604, },
    {'name': 'price', 'type': 'acapellabox', 'voice': 'WillFromAfar',
        'lower': 700, 'upper': 706, },
    {'name': 'price', 'type': 'acapellabox', 'voice': 'WillFromAfar',
        'lower': 22000000, 'upper': 22100000, },

    {'name': 'cageguy', 'type': 'acapellabox', 'voice': 'WillLittleCreature',
        'lower': 27000000, 'upper': 27100000, },
    {'name': 'pickle', 'type': 'acapellabox', 'voice': 'WillLittleCreature',
        'lower': 29000000, 'upper': 29100000, },
    {'name': 'assassin', 'voice': 'gwyneth',
        'lower': 30000000, 'upper': 30100000, },
    {'name': 'hodrick', 'type': 'acapellabox', 'voice': 'Rod',
        'lower': 31000000, 'upper': 31100000, },
    {'name': 'giant', 'type': 'acapellabox', 'voice': 'WillOldMan',
        'lower': 50000000, 'upper': 50000100, },
    {'name': 'giant', 'type': 'acapellabox', 'voice': 'WillOldMan',
        'lower': 531000000, 'upper': 531001202, },

    {'name': 'intro', 'voice': 'russel',
        'lower': 1000000, 'upper': 1000602, },
    {'name': 'firekeeper', 'voice': 'ivy',
        'lower': 2700, 'upper': 3202, },
    {'name': 'firekeeper', 'voice': 'ivy',
        'lower': 2000000, 'upper': 2100000, },
    {'name': 'ludleth', 'voice': 'brian',
        'lower': 3000000, 'upper': 3100000, },
    {'name': 'yuria', 'voice': 'kendra',
        'lower': 4000000, 'upper': 4100000, },
    {'name': 'yoel', 'voice': 'eric',
        'lower': 5000000, 'upper': 5100000, },
    {'name': 'yorshka', 'type': 'acapellabox', 'voice': 'Nelly',
        'lower': 6000000, 'upper': 6100000, },
    {'name': 'hawkwood', 'voice': 'geraint',
        'lower': 7000000, 'upper': 7100000, },
    {'name': 'sirris', 'voice': 'kimberly',
        'lower': 8000000, 'upper': 8100000, },
    {'name': 'eyeguy', 'type': 'acapellabox', 'voice': 'WillSad',
        'lower': 9000000, 'upper': 9100000, },
    {'name': 'andre', 'type': 'acapellabox', 'voice': 'Peter',
        'lower': 10000000, 'upper': 10100000, },
    {'name': 'shrinemaid', 'voice': 'amy',
        'lower': 11000000, 'upper': 11100000, },
    {'name': 'thiefdude', 'voice': 'geraint',
        'lower': 12000000, 'upper': 12100000, },
    {'name': 'sorcerer', 'type': 'acapellabox', 'voice': 'Saul',
        'lower': 13000000, 'upper': 13100100, },
    {'name': 'cornyx', 'type': 'acapellabox', 'voice': 'Micah',
        'lower': 14000000, 'upper': 14100000, },
    {'name': 'karla', 'voice': 'emma',
        'lower': 15000000, 'upper': 15100000, },
    {'name': 'irina', 'voice': 'salli',
        'lower': 16000000, 'upper': 16100000, },
    {'name': 'morne', 'type': 'acapellabox', 'voice': 'WillBadGuy',
        'lower': 17000000, 'upper': 17100000, },
    {'name': 'anri', 'voice': 'nicole',
        'lower': 19000000, 'upper': 19100000, },
    {'name': 'patches', 'type': 'acapellabox', 'voice': 'WillUpClose',
        'lower': 1600, 'upper': 1605, },
    {'name': 'patches', 'type': 'acapellabox', 'voice': 'WillUpClose',
        'lower': 20000000, 'upper': 20100000, },
    {'name': 'siegfried', 'type': 'acapellabox', 'voice': 'PeterHappy',
        'lower': 21000100, 'upper': 21100100, },
    {'name': 'siegfried', 'type': 'acapellabox', 'voice': 'PeterHappy',
        'lower': 2600, 'upper': 2602, },
    {'name': 'emma', 'type': 'acapellabox', 'voice': 'QueenElizabeth',
        'lower': 23000000, 'upper': 23100000, },
    {'name': 'emma', 'type': 'acapellabox', 'voice': 'QueenElizabeth',
        'lower': 1950, 'upper': 1953, },
    {'name': 'emma', 'type': 'acapellabox', 'voice': 'QueenElizabeth',
        'lower': 2450, 'upper': 2453, },

    {'name': 'gael', 'type': 'acapellabox', 'voice': 'WillFromAfar',
        'lower': 51000000, 'upper': 51200000, },
    {'name': 'vilhelm', 'voice': 'brian',
        'lower': 52000000, 'upper': 52100000, },
    {'name': 'paintingwoman', 'voice': 'gwyneth',
        'lower': 53000000, 'upper': 53100000, },
    {'name': 'corviansettler', 'voice': 'eric',
        'lower': 54000000, 'upper': 54100000, },
    {'name': 'friede', 'type': 'acapellabox', 'voice': 'Rosie',
        'lower': 55000000, 'upper': 55100000, },
    {'name': 'arandriel', 'type': 'acapellabox', 'voice': 'WillOldMan',
        'lower': 56000000, 'upper': 56100000, },
    {'name': 'drowsy', 'type': 'acapellabox', 'voice': 'WillHappy',
        'lower': 59000000, 'upper': 59100000, },

    {'name': 'gael', 'type': 'acapellabox', 'voice': 'WillFromAfar',
        'lower': 71000000, 'upper': 71100000, },
    {'name': 'paintingwoman', 'voice': 'gwyneth',
        'lower': 72000000, 'upper': 72100000, },
    {'name': 'lapp', 'voice': 'geraint',
        'lower': 73000000, 'upper': 73100000, },
    {'name': 'shira', 'type': 'acapellabox', 'voice': 'Ella',
        'lower': 74000000, 'upper': 74100000, },
    {'name': 'locust', 'type': 'acapellabox', 'voice': 'WillOldMan',
        'lower': 75000000, 'upper': 75100000, },
    {'name': 'stonehag', 'type': 'acapellabox', 'voice': 'Deepa',
        'lower': 76000000, 'upper': 76100000, },
    {'name': 'hollow', 'type': 'acapellabox', 'voice': 'WillLittleCreature',
        'lower': 77000000, 'upper': 77100000, },
    {'name': 'argo', 'type': 'acapellabox', 'voice': 'WillSad',
        'lower': 78000000, 'upper': 78100000, },
]


exclude = [
    {'language': 'eo', 'name': 'Esperanto'},
    {'language': 'si', 'name': 'Sinhala'},  # swallows words
    {'language': 'id', 'name': 'Indonesian'},  # swallows words
    {'language': 'mi', 'name': 'Maori'},  # swallows words
    {'language': 'nl', 'name': 'Dutch'},
    {'language': 'fr', 'name': 'French'},
]
languages = [
    {'language': 'af', 'name': 'Afrikaans'},
    {'language': 'sq', 'name': 'Albanian'},
    {'language': 'am', 'name': 'Amharic'},
    {'language': 'ar', 'name': 'Arabic'},
    {'language': 'hy', 'name': 'Armenian'},
    {'language': 'az', 'name': 'Azerbaijani'},
    {'language': 'eu', 'name': 'Basque'},
    {'language': 'be', 'name': 'Belarusian'},
    {'language': 'bn', 'name': 'Bengali'},
    {'language': 'bs', 'name': 'Bosnian'},
    {'language': 'bg', 'name': 'Bulgarian'},
    {'language': 'ca', 'name': 'Catalan'},
    {'language': 'ceb', 'name': 'Cebuano'},
    {'language': 'ny', 'name': 'Chichewa'},
    {'language': 'zh', 'name': 'Chinese (Simplified)'},
    {'language': 'zh-TW', 'name': 'Chinese (Traditional)'},
    {'language': 'co', 'name': 'Corsican'},
    {'language': 'hr', 'name': 'Croatian'},
    {'language': 'cs', 'name': 'Czech'},
    {'language': 'da', 'name': 'Danish'},
    {'language': 'nl', 'name': 'Dutch'},
    {'language': 'en', 'name': 'English'},
    {'language': 'eo', 'name': 'Esperanto'},
    {'language': 'et', 'name': 'Estonian'},
    {'language': 'tl', 'name': 'Filipino'},
    {'language': 'fi', 'name': 'Finnish'},
    {'language': 'fr', 'name': 'French'},
    {'language': 'fy', 'name': 'Frisian'},
    {'language': 'gl', 'name': 'Galician'},
    {'language': 'ka', 'name': 'Georgian'},
    {'language': 'de', 'name': 'German'},
    {'language': 'el', 'name': 'Greek'},
    {'language': 'gu', 'name': 'Gujarati'},
    {'language': 'ht', 'name': 'Haitian Creole'},
    {'language': 'ha', 'name': 'Hausa'},
    {'language': 'haw', 'name': 'Hawaiian'},
    {'language': 'iw', 'name': 'Hebrew'},
    {'language': 'hi', 'name': 'Hindi'},
    {'language': 'hmn', 'name': 'Hmong'},
    {'language': 'hu', 'name': 'Hungarian'},
    {'language': 'is', 'name': 'Icelandic'},
    {'language': 'ig', 'name': 'Igbo'},
    {'language': 'id', 'name': 'Indonesian'},
    {'language': 'ga', 'name': 'Irish'},
    {'language': 'it', 'name': 'Italian'},
    {'language': 'ja', 'name': 'Japanese'},
    {'language': 'jw', 'name': 'Javanese'},
    {'language': 'kn', 'name': 'Kannada'},
    {'language': 'kk', 'name': 'Kazakh'},
    {'language': 'km', 'name': 'Khmer'},
    {'language': 'ko', 'name': 'Korean'},
    {'language': 'ku', 'name': 'Kurdish (Kurmanji)'},
    {'language': 'ky', 'name': 'Kyrgyz'},
    {'language': 'lo', 'name': 'Lao'},
    {'language': 'la', 'name': 'Latin'},
    {'language': 'lv', 'name': 'Latvian'},
    {'language': 'lt', 'name': 'Lithuanian'},
    {'language': 'lb', 'name': 'Luxembourgish'},
    {'language': 'mk', 'name': 'Macedonian'},
    {'language': 'mg', 'name': 'Malagasy'},
    {'language': 'ms', 'name': 'Malay'},
    {'language': 'ml', 'name': 'Malayalam'},
    {'language': 'mt', 'name': 'Maltese'},
    {'language': 'mi', 'name': 'Maori'},
    {'language': 'mr', 'name': 'Marathi'},
    {'language': 'mn', 'name': 'Mongolian'},
    {'language': 'my', 'name': 'Myanmar (Burmese)'},
    {'language': 'ne', 'name': 'Nepali'},
    {'language': 'no', 'name': 'Norwegian'},
    {'language': 'ps', 'name': 'Pashto'},
    {'language': 'fa', 'name': 'Persian'},
    {'language': 'pl', 'name': 'Polish'},
    {'language': 'pt', 'name': 'Portuguese'},
    {'language': 'pa', 'name': 'Punjabi'},
    {'language': 'ro', 'name': 'Romanian'},
    {'language': 'ru', 'name': 'Russian'},
    {'language': 'sm', 'name': 'Samoan'},
    {'language': 'gd', 'name': 'Scots Gaelic'},
    {'language': 'sr', 'name': 'Serbian'},
    {'language': 'st', 'name': 'Sesotho'},
    {'language': 'sn', 'name': 'Shona'},
    {'language': 'sd', 'name': 'Sindhi'},
    {'language': 'si', 'name': 'Sinhala'},
    {'language': 'sk', 'name': 'Slovak'},
    {'language': 'sl', 'name': 'Slovenian'},
    {'language': 'so', 'name': 'Somali'},
    {'language': 'es', 'name': 'Spanish'},
    {'language': 'su', 'name': 'Sundanese'},
    {'language': 'sw', 'name': 'Swahili'},
    {'language': 'sv', 'name': 'Swedish'},
    {'language': 'tg', 'name': 'Tajik'},
    {'language': 'ta', 'name': 'Tamil'},
    {'language': 'te', 'name': 'Telugu'},
    {'language': 'th', 'name': 'Thai'},
    {'language': 'tr', 'name': 'Turkish'},
    {'language': 'uk', 'name': 'Ukrainian'},
    {'language': 'ur', 'name': 'Urdu'},
    {'language': 'uz', 'name': 'Uzbek'},
    {'language': 'vi', 'name': 'Vietnamese'},
    {'language': 'cy', 'name': 'Welsh'},
    {'language': 'xh', 'name': 'Xhosa'},
    {'language': 'yi', 'name': 'Yiddish'},
    {'language': 'yo', 'name': 'Yoruba'},
    {'language': 'zu', 'name': 'Zulu'}
]
