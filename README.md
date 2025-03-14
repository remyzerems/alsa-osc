# alsa-osc bridge
Control audio interface ALSA parameters (like volume, mute, record...) using OSC protocol.

# What is it for ?
This script allows controlling any available parameter of any audio interface connected to a Linux computer running ALSA audio backend.
The control is made using [OSC protocol](https://fr.wikipedia.org/wiki/Open_Sound_Control) commands.

In other words, you can for example install [TouchOSC](https://play.google.com/store/apps/details?id=net.hexler.lex&hl=fr) or [OSC Controller](https://play.google.com/store/apps/details?id=com.ffsmultimedia.osccontroller&hl=fr) on your Android phone and control the playback volume of your computer.

# Who is this for ?
It's intended to be used by audio engineers or music makers, but could of course be used by many other people who'd like to control their audio interface parameters from an OSC capable application/device.


# Prerequisites
In order to get this working, you need to have Python3 installed which should already be installed if you're using Linux.
You also need to have pip3 installed. It's the Python package manager.

Then you need to install the Python libraries
* pyalsaaudio
```bash
pip3 install --no-cache-dir --upgrade pyalsaaudio
```
* python-osc
```bash
pip3 install python-osc
```

# Installing
Simply download the alsa-osc files and place the files in the folder of you choice.

# Running
Open a terminal.
Using cd command, move to the folder where the script files are stored and run the script:
```bash
python3 alsa-osc.py
```

The script enumerates all the OSC routes found, that you can call to change a parameter for example:
```bash
Creating OSC routes for ALSA controls:
Audio interface: USB Audio CODEC
        'PCM' control
                Volume control route: /alsa/interface/USB Audio CODEC/PCM
                        Channel 0 control: /alsa/interface/USB Audio CODEC/PCM/CH0
                        Channel 1 control: /alsa/interface/USB Audio CODEC/PCM/CH1
                        Min value: 0
                        Max value: 128
                Volume control in dB route: /alsa/interface/USB Audio CODEC/PCM/dB
                        Channel 0 control: /alsa/interface/USB Audio CODEC/PCM/dB/CH0
                        Channel 1 control: /alsa/interface/USB Audio CODEC/PCM/dB/CH1
                        Min value: -128.0
                        Max value: 0.0
                Mute control route: /alsa/interface/USB Audio CODEC/PCM/mute
                        1 to mute, 0 to unmute

Serving OSC on ('0.0.0.0', 8000)
```

On the OSC controller, you'll have to type in the routes so that the software knows which route to use to control a given parameter.

# Testing
If you don't have an OSC controller at hand, you can run the test-alsa-osc.py script which will call a route.
You'll have to tweak it a little bit so that it matches the routes found on your interfaces.
Change those lines to match what has been detected from your interfaces.
```python
card_name = "USB Audio CODEC"  # Name of the audio interface
control = "PCM"  # ALSA control name (e.g. "Master", "PCM", etc.)
```

Then run the script:
```bash
python3 test-alsa-osc.py
```
