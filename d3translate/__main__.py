'''Dark Souls 3 Translation Scrambler'''
# pylint: disable=C0413,C0103,C0111

import asyncio
import datetime
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import fsb5
import paco

from . import data


print('d3translate 0.1')
print()

if not data.credentialspath.is_file():
    print('No Google credentials found in', data.credentialspath)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(data.credentialspath)
print('loading google api credentials', os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
print()


from .processor import Processor
from .voicegen import Voicegen

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


if data.outputpath.is_dir() and any(data.outputpath.iterdir()):
    print('output directory', data.outputpath, 'not empty!')
    sys.exit(1)


# buildpath cleanup
print('cleaning up build directory', data.buildpath)
print()
data.buildpath.mkdir(exist_ok=True)
for path in data.buildpath.iterdir():
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=False)
    else:
        path.unlink()
data.outputpath.mkdir(exist_ok=True)


# copy dcx archices to build
for file in (d for d in data.textpath.glob('*.dcx') if d.is_file()):
    shutil.copy(file, data.buildpath)
# unpack dcx archives
for file in (x for x in data.buildpath.iterdir() if x.is_file() and x.suffix == '.dcx'):
    print('unpacking', file.relative_to(data.basepath))
    subprocess.call([r'tools/yabber/Yabber.exe', str(file)], stdout=subprocess.DEVNULL)
    file.unlink()
# walk subdirs and unpack fmg files
print('unpacking fmg files')
for file in data.buildpath.glob('**/*.fmg'):
    subprocess.call([r'tools/yabber/Yabber.exe', str(file)], stdout=subprocess.DEVNULL)
    print('.', sep='', end='', flush=True)
print()

def count_xmls():
    processor = Processor()
    for xml in data.buildpath.glob('**/*.fmg.xml'):
        processor.count(xml)
    print()

    print('lines to translate:', processor.linecount)
    print('chars to translate:', processor.charcount)
    print()

print('checking xmls in', data.buildpath.relative_to(data.basepath))
count_xmls()


# translate xml entries
async def translate_xmls():
    starttime = time.time()

    processor = Processor()
    for xml in data.buildpath.glob('**/*.fmg.xml'):
        await processor.translate(xml)

    endtime = time.time()

    print('lines translated:', processor.linecount)
    print('chars translated:', processor.charcount)
    print('took %.3f seconds' % (endtime - starttime))
    print()

print('translating xmls in', data.buildpath.relative_to(data.basepath))
print()
asyncio.run(translate_xmls(), debug=False)


# decrypt voice fsbs
async def decrypt_fsb(fsb: Path):
    print('decrypting', fsb.name, 'to', data.buildpath.relative_to(data.basepath))
    return await (await asyncio.create_subprocess_exec(
        str(data.basepath.joinpath('tools/fsbext/fsbext.exe').resolve()),
        '-e', 'FDPrVuT4fAFvdHJYAgyMzRF4EcBAnKg', '1',
        str(fsb.resolve()),
        cwd=str(data.buildpath.resolve()),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )).wait()
async def decrypt_all():
    await paco.map(decrypt_fsb, list(data.soundpath.glob('fdp_vm*.fsb')), limit=16)
    print()
asyncio.run(decrypt_all(), debug=False)


# rebuild fsbs
def regenerate_fsb(inputpath: Path, voicegen: Voicegen):
    print('reading', inputpath)
    build_successes_ = []
    build_failures_ = []

    with open(str(inputpath), 'rb') as f:
        fsb = fsb5.FSB5(f.read())
    name = inputpath.name[:-10]

    lstpath = data.buildpath.joinpath(name + '.lst')
    fsbpath = data.outputpath.joinpath(name + '.fsb')

    samplenames = list(map(lambda sample: sample.name, fsb.samples))
    with open(lstpath, 'w') as lst:
        for sample in samplenames:
            lst.write("%s\n" % sample)

    # extract existing audio
    print('extracting samples')
    subprocess.check_call([
        str(data.basepath.joinpath('tools/fmodextr/fmod_extr.exe').resolve()), str(file.resolve())
    ], cwd=str(data.buildpath.resolve()), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print('generating', len(samplenames), 'voicelines')
    asyncio.run(voicegen.genallvoicelines(samplenames), debug=False)

    print('generating', fsbpath.relative_to(data.outputpath).name)
    result = subprocess.call([
        str(data.basepath.joinpath('tools/fmod/fsbankcl.exe').resolve()), '-o', str(fsbpath),
        '-quality', '98', '-encryption_key', 'FDPrVuT4fAFvdHJYAgyMzRF4EcBAnKg',
        '-format', 'vorbis', '-thread_count', '8', '-rebuild', '-verbosity', '0',
        str(lstpath)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result != 0:
        print('failed building soundbank:', lstpath)
        build_failures_ += [fsbpath]
    else:
        print('sucessfully built soundbank:', lstpath)
        build_successes_ += [fsbpath]

    # shutil.rmtree(data.buildpath, ignore_errors=True)
    print()
    return build_failures_, build_successes_

voice_generator = Voicegen()
build_successes = []
build_failures = []
for file in data.buildpath.glob('*_crypt.fsb'):
    fails, succs = regenerate_fsb(file, voice_generator)
    build_failures += fails
    build_successes += succs


# finish up

print('sucessfully built', len(build_successes), 'sound banks')
if build_failures:
    print('failed building', len(build_failures), 'sound banks:')
    print('\t', '\n\t'.join(build_failures))
print()


# walk subdirs and repack fmg files
print('repacking fmg files')
for file in data.buildpath.glob('**/*.fmg.xml'):
    subprocess.call([r'tools/yabber/Yabber.exe', str(file)], stdout=subprocess.DEVNULL)
    print('.', sep='', end='', flush=True)
print()
# repack dcx archives
for file in (x for x in data.buildpath.iterdir() if x.is_dir() and '-msgbnd-dcx' in x.name):
    print('repacking', file.relative_to(data.basepath))
    subprocess.call([r'tools/yabber/Yabber.exe', str(file)], stdout=subprocess.DEVNULL)
# move repacked dcx dirs to output
for file in (x for x in data.buildpath.iterdir() if x.is_file() and x.suffix == '.dcx'):
    print('copying', file.relative_to(data.basepath),\
        'to', data.outputpath.relative_to(data.basepath))
    shutil.copy(file, data.outputpath)


print()
print(
    '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +']',
    'process completed! see', data.outputpath, 'for results')
