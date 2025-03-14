"""
MIT License

Copyright (c) 2025 remyzerems (https://github.com/remyzerems/alsa-osc)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
This script tests calling the OSC server to request Alsa controls changes
"""

from pythonosc import udp_client

OSC_SERVICE_ROOT = "/alsa/interface"

osc_service_ip = "127.0.0.1"
osc_service_port = 8000

# Create an OSC client that will connect to the OSC server
client = udp_client.SimpleUDPClient(osc_service_ip, osc_service_port)

card_name = "USB Audio CODEC"  # Name of the audio interface
control = "PCM"  # ALSA control name (e.g. "Master", "PCM", etc.)

# Adjust volume
address = f"{OSC_SERVICE_ROOT}/{card_name}/{control}"
value = 0.86  # Volume to set
#client.send_message(address, value)    # Uncomment this line to set the volume

# Adjust the volume using dB scale
address = f"{OSC_SERVICE_ROOT}/{card_name}/{control}/dB"
value = -18.0  # Volume value in dB
#client.send_message(address, value)     # Uncomment this line to set the volume

# Mute/unmute
mute_address = f"{OSC_SERVICE_ROOT}/{card_name}/{control}/mute"
mute_value = True  # True to mute, False to unmute
client.send_message(mute_address, mute_value)
