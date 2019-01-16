# Dark Souls 3 Translation Scrambler

A scrambled translation generator for Dark Souls 3.

Used to generate [Dark Souls 3 Poorly Translated Edition](https://www.nexusmods.com/darksouls3/mods/316/).


## Description

This program takes all text from the game Dark Souls 3, runs it through Google Translate with randomly selected languages multiple times, and generates new audio for character voicelines.

You can generate your very own "poor translation edition" with this.


## Usage

Some preparations and adjustments have to be made before this can be run:

* Install python requirements with `pip install -r requirements.txt`
* Unpack the game files with [UXM](https://github.com/JKAnderson/UXM)
* Copy the dcx files from `<gamepath>/msg/engus` to `input/msg/engus`
* Copy the voice fsb files (`fdp_vm*.fsb`) from `<gamepath>/sound` to `input/sound`
* Download your Google Cloud Platform API key and save it as `google.credentials.json`
* Set your Cloud Translation API quotas to at least 5 million
* Configure voice selections for characters in `d3translate/data.py` based on system voices you have installed

After that d3translate can be run with `python -m d3translate`.
The resulting files can then be found under `output`.

Note: With default settings (5 random language steps) and a standard Dark Souls 3 installation, the whole translation process will translate around 5 million characters. See [Cloud Translation API pricing](https://cloud.google.com/translate/pricing?hl=de) for consideration.


## Acknowledgements

* JKAnderson for creating [UXM](https://github.com/JKAnderson/UXM) and [Yabber](https://github.com/JKAnderson/Yabber)
* Luigi Auriemma for creating [fsbext](http://aluigi.altervista.org/search.php?src=fsbext)
* id-daemon for creating fmod_extr
* Simon Pinfold for creating [python-fsb5](https://github.com/HearthSim/python-fsb5)
* Firelight Technologies for making fsbankcl openly available

