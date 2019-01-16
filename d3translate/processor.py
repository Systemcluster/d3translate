'''Dark Souls 3 msg XML processor'''
# pylint: disable=E1101,E1136,E1137,C0111,C0103

import asyncio
import codecs
import random
import re
import time
from dataclasses import dataclass, field
from functools import partial, reduce, wraps
from pathlib import Path
from typing import Dict
from xml.etree import ElementTree

import paco

from . import data
from .translator import Translator


def wrapasync(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run

def replacenth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    return before + after

@dataclass
class Processor:
    linecount: int = 0
    charcount: int = 0
    cachcount: int = 0
    collcount: int = 0
    textcache: Dict[str, str] = field(default_factory=dict)
    rand: random.Random = random.Random()

    def reset(self):
        self.linecount = 0
        self.charcount = 0
        self.cachcount = 0
        self.collcount = 0
        self.textcache = {}

    @staticmethod
    def getentries(path: Path) -> (ElementTree, ElementTree):
        '''Get all entries from a msg xml'''
        # exclude certain paths
        skip = False
        for e in data.ignorefiles_prefix:
            if path.name.startswith(e):
                skip = True
                break
        if skip:
            return None, None

        xml = ElementTree.parse(path)
        root = xml.getroot()
        if not root or root.tag != 'fmg':
            print('invalid fmg xml! no fmg root in', path)
            return None, None
        entries = root.find('entries')
        if not entries:
            print('invalid fmg xml! no entries in', path)
            return None, None
        for entry in entries:
            if not entry.text:
                entry.text = ' '

        # exclude certain texts
        return (xml, list(filter(
            lambda entry: \
                entry.text not in data.ignoretext and \
                not any(filter(lambda infix: infix in entry.text, data.ignoretext_infix)),
            entries)))

    @staticmethod
    def savexml(xml: ElementTree, path: Path):
        '''Save xml in the correct format'''
        print()
        print('writing   ', path.relative_to(data.basepath))
        xml.write(path, encoding='utf-8', xml_declaration=False)
        # prepend bom and correct decl
        with codecs.open(path, 'r', 'utf-8') as original:
            ogdata = original.read()
        with codecs.open(path, 'w', 'utf-8-sig') as modified:
            modified.write('<?xml version="1.0" encoding="utf-8"?>\n' + ogdata)

    @wrapasync
    def __translate_entry(self, entry: ElementTree) -> int:
        text = entry.text

        # check if translation is already cached
        if text in self.textcache.keys():
            entry.text = self.textcache[text]
            print('#', sep='', end='', flush=True)
            return -1

        # send text for translation
        t = Translator(text, self.rand)
        t.run(data.translate_steps)

        # reorder into separate lines

        original_text_lines = text.splitlines()
        original_break = 0
        for line in original_text_lines:
            if line == '':
                break
            lsp = line.split('. ')
            if not lsp:
                if line[-1:] == '.':
                    original_break += 1
            else:
                original_break += len(lsp)
        else:
            original_break = 0

        if len(original_text_lines) > 2:
            res = '\n'.join(map(lambda r: r[:1].upper() + r[1:],\
                t.string.replace('. ', '.\n', len(original_text_lines) - 1).splitlines()))
            if original_break and res.count('\n') >= original_break:
                res = replacenth(res, '\n', '\n\n', original_break)
                if original_break > 1:
                    res = res.replace('.\n', '. ', 1)
        # elif len(original_text_lines) > 1:
        #     res = t.string.replace('. ', '.\n', 1).replace('\n\n', '\n')
        else:
            res = t.string

        # check if translation is already cached
        # in case same text was sent for translation simultaniously
        if text in self.textcache.keys():
            entry.text = self.textcache[text]
            print('!', sep='', end='', flush=True)
            return -2

        # store results
        entry.text = res
        self.textcache[text] = res
        print('.', sep='', end='', flush=True)
        return len(text)


    async def translate(self, path: Path):
        xml, entries = self.getentries(path)
        if not xml:
            print('skipping', path.relative_to(data.basepath))
            return
        if not entries:
            print('skipping', path.relative_to(data.basepath))
            self.savexml(xml, path)
            return
        print('processing', path.relative_to(data.basepath), 'with', len(entries), 'entries')

        starttime = time.time()

        # shuffle because often the same entry appears multiple time in a row
        # and we want to minimize concurrency collisions
        entries_shuffled = list(entries)
        random.shuffle(entries_shuffled)

        results = await paco.map(self.__translate_entry, entries_shuffled, limit=32)
        linecount = reduce(lambda a, v: a+1, filter(lambda v: v > 0, results), 0)
        charcount = reduce(lambda a, v: a+v, filter(lambda v: v > 0, results), 0)
        cachcount = reduce(lambda a, v: a+1, filter(lambda v: v == -1, results), 0)
        collcount = reduce(lambda a, v: a+1, filter(lambda v: v == -2, results), 0)

        self.linecount += linecount
        self.charcount += charcount
        self.cachcount += cachcount
        self.collcount += collcount

        self.savexml(xml, path)

        endtime = time.time()
        print('processed %d lines with %d chars in %.3f seconds (%d cached, %d collisions)' %\
            (linecount, charcount, endtime - starttime, cachcount, collcount))
        print()


    def count(self, path: Path):
        _, entries = self.getentries(path)
        if not entries:
            # print('\tskipping', path)
            return
        # print('\tcounting', path)
        # starttime = time.time()

        linecount = 0
        charcount = 0
        cachcount = 0
        for entry in entries:
            text = entry.text

            if not text in self.textcache.keys():
                self.textcache[text] = 'c'
                linecount += 1
                charcount += len(text)
            else:
                cachcount += 1

        self.linecount += linecount
        self.charcount += charcount
        self.cachcount += cachcount

        # endtime = time.time()
        # print('\tcounted %d unique lines with %d chars in %.3f seconds (%d cached)' %\
        #     (linecount, charcount, endtime - starttime, cachcount))
