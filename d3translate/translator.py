'''Google chain Translator'''
# pylint: disable=W0703,C0103

import random
import re
from typing import Dict, List

from google.cloud import translate

from . import data


TRANSLATE_CLIENT = translate.Client()

class Translator:
    '''Google chain Translator'''

    defaultlang = {'language': 'en', 'name': 'English'}

    def __init__(
            self,
            source: str,
            rand: random.Random = None,
            sourcelang: Dict = None):

        if not sourcelang:
            sourcelang = self.defaultlang
        self.source: str = source
        self.string: str = source
        self.used: List = [sourcelang]
        self.lastlang: str = ''
        self.lang: str = sourcelang
        self.next = [
            # {'language': 'ja', 'name': 'Japanese'},
            None,
        ]
        if rand:
            self.rand = rand
        else:
            self.rand = random.Random()

    def __setrandomlanguage(self):
        while not self.lang or self.lang in self.used or self.lang in data.exclude:
            self.lang = self.rand.choice(data.languages)

    def __translate(self, lang: Dict = None):
        if lang:
            self.lang = lang
        elif self.next:
            self.lang = self.next.pop()
            if not self.lang:
                self.__setrandomlanguage()
        else:
            self.__setrandomlanguage()

        done = False
        while not done:
            try:
                translation = {}
                if self.lastlang:
                    # print()
                    # print('translating from %s to %s' %(self.lastlang['name'], self.lang['name']))
                    translation = TRANSLATE_CLIENT.translate(
                        self.string,
                        target_language=self.lang['language'],
                        source_language=self.lastlang['language']
                    )
                else:
                    # print()
                    # print('translating from ? to %s' %(self.lang['name']))
                    translation = TRANSLATE_CLIENT.translate(
                        self.string,
                        target_language=self.lang['language']
                    )
            except Exception as e:
                print()
                input('translation failed, press return to retry... (' + str(e) + ')')
                continue
            done = True

        self.string = translation['translatedText']
        self.string = self.string.replace('&#39;', '\'')
        self.string = self.string.replace('&quot;', '"')
        self.lastlang = self.lang
        self.used += [self.lang]

        # print('result:', self.string)


    def run(self, times: int) -> str:
        '''Run translation process'''

        # print()
        # print(self.string)

        for _ in range(0, times):
            self.__translate()
        self.__translate(self.defaultlang)

        repl = ['.', ',', '!', '?', ':', ';']

        if self.source.endswith('.') and not any(self.string.endswith(x) for x in repl):
            self.string = self.string + '.'

        if self.source.endswith('-') and not self.string.endswith('-'):
            if self.string.endswith('.'):
                self.string = self.string[:-1]
            self.string = self.string + '-'

        if self.source.endswith('!') and not self.string.endswith('!'):
            if any(self.string.endswith(x) for x in ['.', ',', ':', ';']):
                self.string = self.string[:-1]
            self.string = self.string + '!'

        if self.source.endswith('?') and not self.string.endswith('?'):
            if any(self.string.endswith(x) for x in ['.', ',', ':', ';']):
                self.string = self.string[:-1]
            self.string = self.string + '?'

        if self.source[:1].isupper():
            self.string = re.sub('^([a-zA-Z])', lambda x: x.groups()[0].upper(), self.string, 1)
        else:
            self.string = re.sub('^([a-zA-Z])', lambda x: x.groups()[0].lower(), self.string, 1)

        # print()
        # print('original:', self.source)
        # print('result:', self.string)

        return self.string
