'''Audio generator for Voicelines'''
# pylint: disable=C0103

import asyncio
import os
import random
import shutil
import subprocess
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import paco

from . import data
from .processor import Processor



def _speak(wavpath, voice_, voiceconfig, text):
    '''standalone sapi.spvoice to file'''
    import comtypes.client

    voice = None
    for v in comtypes.client.CreateObject("SAPI.SpVoice").GetVoices():
        if all(x in v.GetDescription().lower() for x in data.voicefilter + [voice_.lower()]):
            voice = v
            break
    if not voice:
        raise Exception('voice not found: ' + voice_)

    speak = comtypes.client.CreateObject("SAPI.SpVoice")
    speak.Voice = voice
    if 'rate' in voiceconfig:
        speak.Rate = voiceconfig['rate']

    filestream = comtypes.client.CreateObject("SAPI.SpFileStream")
    audioformat = comtypes.client.CreateObject("SAPI.SpAudioFormat")
    audioformat.Type = 34 # 44kHz 16bit mono
    filestream.Format = audioformat

    filestream.Open(str(wavpath), 3, False)
    speak.AudioOutputStream = filestream
    speak.Speak(text)
    filestream.close()


def _speak_acapellabox(mp3path, voice, text):
    '''standalone acapelladownloader to file'''
    return subprocess.call([
        str(data.basepath.joinpath('tools/acapelladownloader/AcapellaDownloader.exe').resolve()),
        '-v', voice, '-t', text, '-p', str(mp3path.resolve())],
        cwd=str(data.buildpath.resolve()),
        stdout=subprocess.DEVNULL
    )


@dataclass
class VoiceEntry:
    '''XML voice entry representation'''
    id: int
    text: str
    file: Path


class Voicegen:
    '''Audio generator for Voicelines'''

    def __init__(self):
        self.voicelines: Dict[int, VoiceEntry] = {}
        self.voicecache = {}
        self.executor: ProcessPoolExecutor = ProcessPoolExecutor()
        self.limit = 24
        self.acapellalock = asyncio.Lock()
        self.samplebank = ''

        print('collecting voicelines from', data.buildpath)
        allentries: List[VoiceEntry] = []
        for xml in data.buildpath.glob('**/*.fmg.xml'):
            # filter out non-voiceline xmls
            if not any(filter(xml.name.startswith, data.voicefiles_prefix)):
                continue
            print('\t', xml.relative_to(data.buildpath))
            _, entries = Processor.getentries(xml)
            # pylint: disable=W0640
            allentries += list(map(lambda e: VoiceEntry(int(e.get('id')), e.text, xml), entries))

        listentries: Dict[int, List[VoiceEntry]] = defaultdict(list)
        for entry in allentries:
            listentries[entry.id].append(entry)

        # check conflicting voicelines
        for entry_id, entries in listentries.items():
            self.voicelines[entry_id] = entries[0]
            if len(entries) > 1:
                conflicts = []
                for entry in entries:
                    if len(list(filter(lambda v: v.text == entry.text, entries))) == len(entries):
                        continue
                    conflicts += [entry]
                if conflicts:
                    print('conflicting entries for id', entry_id)
                    print('\t', '\n\tin file '.join(map(lambda entry: \
                        str(entry.file.relative_to(data.buildpath))\
                        + ': ' + entry.text, conflicts)))

        print('found', len(self.voicelines), 'unique voice lines')
        print()


    @staticmethod
    def mapvoiceid(voiceid: int):
        '''Map unusual voiceids to their subtitle ids'''
        if voiceid >= 51100000 and voiceid < 51200000:
            return voiceid - 100000
        if voiceid == 90000000:
            return 17001704
        if voiceid == 531000000:
            return 50000000
        if voiceid == 531001202:
            return 50000100
        return voiceid

    def getvoiceline(self, voiceid: int):
        '''Get a specific voice line'''
        voiceid_ = self.mapvoiceid(voiceid)
        if voiceid_ in self.voicelines:
            return self.voicelines[voiceid_]
        return None

    async def genallvoicelines(self, samplenames, samplebank):
        '''Generate all voice lines for given samples, multiprocessed'''
        samplenames_ = samplenames
        self.samplebank = samplebank[:8]
        random.shuffle(samplenames_)
        await paco.map(self.__genvoicelineasync, samplenames_, limit=self.limit)
        print()


    def testvoices(self):
        '''Speak a random line in all available voices'''
        import comtypes.client
        voices = list(filter(
            lambda v: all(x in v.GetDescription().lower() for x in data.voicefilter),
            comtypes.client.CreateObject("SAPI.SpVoice").GetVoices()))
        line = random.choice(list(self.voicelines.values()))
        print('selected line', line)
        for voice in voices:
            print('speaking with', voice.GetDescription())
            speak = comtypes.client.CreateObject("SAPI.SpVoice")
            speak.Voice = voice
            speak.Speak(line.text)


    async def __genvoicelineasync(self, samplename_: str):
        result_ = await self.__genvoiceline(samplename_)
        if result_ == -2:
            # could not generate audiofile, use dummy audio instead
            audio = data.buildpath.joinpath(samplename_).resolve()
            shutil.copyfile(data.basepath.joinpath('dummy.mp3').resolve(), audio)


    def __getvoice(self, voiceid: int):
        if voiceid in self.voicecache:
            return self.voicecache[voiceid]
        for voiceconfig in data.voices:
            if voiceid >= voiceconfig['lower'] and voiceid <= voiceconfig['upper']:
                self.voicecache[voiceid] = voiceconfig
                return self.voicecache[voiceid]
        self.voicecache[voiceid] = data.voices[0]
        return self.voicecache[voiceid]


    async def __genvoiceline(self, samplename: str) -> int:
        mp3path: Path = data.buildpath.joinpath(samplename).resolve()
        wavpath: Path = data.buildpath.joinpath(samplename+'.wav').resolve()

        # check if sample is excluded
        if samplename in data.voice_sample_excludes:
            if self.samplebank in data.voice_sample_excludes[samplename]:
                if wavpath.is_file():
                    if mp3path.is_file():
                        mp3path.unlink()
                        print('`', sep='', end='', flush=True)
                    # convert audio
                    await self.__convertaudio(wavpath, mp3path)
                    print('*', sep='', end='', flush=True)
                    return -1
                print('x', sep='', end='', flush=True)
                return -2
            else:
                forceregen = True
        else:
            forceregen = False

        # check if target already exists
        if mp3path.is_file():
            if not forceregen:
                print('#', sep='', end='', flush=True)
                return 0
            else:
                mp3path.unlink()
                print('`', sep='', end='', flush=True)

        # check if sample name corresponds to a valid voice id
        try:
            voiceid = int(samplename[1:10])
        except ValueError:
            if wavpath.is_file():
                # convert audio
                await self.__convertaudio(wavpath, mp3path)
                print('?', sep='', end='', flush=True)
                return -1
            print('x', sep='', end='', flush=True)
            return -2

        # check if text for voiceline exists
        voiceline = self.getvoiceline(voiceid)
        if not voiceline:
            if wavpath.is_file():
                # convert audio
                await self.__convertaudio(wavpath, mp3path)
                print('?', sep='', end='', flush=True)
                return -1
            print('x', sep='', end='', flush=True)
            return -2
        text = voiceline.text

        voiceconfig = self.__getvoice(voiceid)
        voice = voiceconfig['voice']
        mode = voiceconfig['type'] if 'type' in voiceconfig else 'spvoice'
        if mode == 'acapellabox':
            # acepellabox blocks concurrent access
            async with self.acapellalock:
                result = 1
                while result != 0:
                    result = _speak_acapellabox(mp3path, voice, text)
                    if result != 0:
                        print('\nsample generation failed, trying again... (' + \
                        str(result) + ')')
                        await asyncio.sleep(random.randint(1, 3))
        elif mode == 'spvoice':
            # speak voiceline to file
            await asyncio.gather(asyncio.get_running_loop().run_in_executor(
                self.executor, _speak, wavpath, voice, voiceconfig, text))
            # convert audio
            await self.__convertaudio(wavpath, mp3path)
            wavpath.unlink()
        else:
            raise Exception('wrong voicegen mode')


        print('.', sep='', end='', flush=True)
        return 0


    async def __convertaudio(self, source: Path, dest: Path):
        # convert to mp3 so fsbankcl.exe doesn't trip
        return await (await asyncio.create_subprocess_exec(
            str(data.basepath.joinpath('tools/ffmpeg/ffmpeg.exe').resolve()), '-i', str(source),
            '-f', 'mp3', '-ac', '1', '-ar', '48000', '-loglevel', 'quiet', str(dest),
            env={'PATH': os.getenv('PATH')}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )).wait()
