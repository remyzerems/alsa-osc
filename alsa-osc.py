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
alsa-osc bridge

Control audio interface ALSA parameters (like volume, mute, record...) using OSC protocol.
"""

import alsaaudio
from pythonosc import dispatcher
from pythonosc import osc_server

OSC_SERVICE_IP = "0.0.0.0"
OSC_SERVICE_PORT = 8000

OSC_SERVICE_ROOT = "/alsa/interface"


"""
OSC route endpoints
"""
# Setting volume
def set_alsa_control(card_index, control_name, value, channel, units):
    mixer = alsaaudio.Mixer(control_name, cardindex=card_index)
    mixer.setvolume(int(value * 100), channel=channel, units=units)

# Muting/unmuting
def mute_alsa_control(card_index, control_name, mute):
    mixer = alsaaudio.Mixer(control_name, cardindex=card_index)
    mixer.setmute(1 if mute else 0)

# Record arm set/unset
def rec_alsa_control(card_index, control_name, rec):
    mixer = alsaaudio.Mixer(control_name, cardindex=card_index)
    mixer.setrec(1 if rec else 0)


"""
OSC route handlers
"""
def create_osc_volume_handler(card_index, control_name, channel=alsaaudio.MIXER_CHANNEL_ALL, units=alsaaudio.VOLUME_UNITS_PERCENTAGE):
    def handler(unused_addr, value):
        set_alsa_control(card_index, control_name, value, channel, units)
    return handler

def create_osc_mute_handler(card_index, control_name):
    def handler(unused_addr, mute):
        mute_alsa_control(card_index, control_name, mute)
    return handler

def create_osc_rec_handler(card_index, control_name):
    def handler(unused_addr, rec):
        rec_alsa_control(card_index, control_name, rec)
    return handler



def list_alsa_controls():
    controls = {}
    for card_index, card_name in enumerate(alsaaudio.cards()):
        card_controls = alsaaudio.mixers(cardindex=card_index)
        controls[card_index] = []
        for control_name in card_controls:
            mixer = alsaaudio.Mixer(control_name, cardindex=card_index)

            volumes = mixer.getvolume()
            channel_count = len(volumes)

            pmin_default, pmax_default = mixer.getrange()

            pmin_dB, pmax_dB = mixer.getrange(units=alsaaudio.VOLUME_UNITS_DB)
            pmin_dB = pmin_dB / 100.0
            pmax_dB = pmax_dB / 100.0

            can_mute = 'mute' in mixer.switchcap() or 'Mute' in mixer.switchcap() or 'Playback Mute' in mixer.switchcap()
            can_rec = 'Capture Mute' in mixer.switchcap()

            controls[card_index].append((control_name, channel_count, can_mute, can_rec, pmin_default, pmax_default, pmin_dB, pmax_dB))
    return controls

def main():
    controls = list_alsa_controls()
    dispatch = dispatcher.Dispatcher()

    print("Creating OSC routes for ALSA controls:")
    for card_index, control_list in controls.items():
        (card_name, card_longname) = alsaaudio.card_name(card_index)
        print(f"Audio interface: {card_name}")
        if len(control_list) > 0:
            for control_name, channel_count, can_mute, can_rec, pmin_default, pmax_default, pmin_dB, pmax_dB in control_list:
                print(f"\t'{control_name}' control")

                route = f"{OSC_SERVICE_ROOT}/{card_name}/{control_name}"
                dispatch.map(route, create_osc_volume_handler(card_index, control_name))
                print(f"\t\tVolume control route: {route}")
                if channel_count > 1:
                    for channel in range(0, channel_count):
                        route = f"{OSC_SERVICE_ROOT}/{card_name}/{control_name}/CH{channel}"
                        dispatch.map(route, create_osc_volume_handler(card_index, control_name, channel))
                        print(f"\t\t\tChannel {channel} control: {route}")
                print(f"\t\t\tMin value: {pmin_default}")
                print(f"\t\t\tMax value: { pmax_default}")

                route = f"{OSC_SERVICE_ROOT}/{card_name}/{control_name}/dB"
                dispatch.map(route, create_osc_volume_handler(card_index, control_name, units=alsaaudio.VOLUME_UNITS_DB))
                print(f"\t\tVolume control in dB route: {route}")
                if channel_count > 1:
                    for channel in range(0, channel_count):
                        route = f"{OSC_SERVICE_ROOT}/{card_name}/{control_name}/dB/CH{channel}"
                        dispatch.map(route, create_osc_volume_handler(card_index, control_name, channel, alsaaudio.VOLUME_UNITS_DB))
                        print(f"\t\t\tChannel {channel} control: {route}")
                print(f"\t\t\tMin value: {pmin_dB}")
                print(f"\t\t\tMax value: { pmax_dB}")

                if can_mute:
                    mute_route = f"{OSC_SERVICE_ROOT}/{card_name}/{control_name}/mute"
                    dispatch.map(mute_route, create_osc_mute_handler(card_index, control_name))
                    print(f"\t\tMute control route: {mute_route}")
                    print(f"\t\t\t1 to mute, 0 to unmute")
                if can_rec:
                    rec_route = f"{OSC_SERVICE_ROOT}/{card_name}/{control_name}/rec"
                    dispatch.map(rec_route, create_osc_rec_handler(card_index, control_name))
                    print(f"\t\tRec control route: {rec_route}")
                    print(f"\t\t\t1 to record arm, 0 to unset")
        else:
            print("\tNo controls found...")
        print()

    server = osc_server.ThreadingOSCUDPServer((OSC_SERVICE_IP, OSC_SERVICE_PORT), dispatch)
    print(f"Serving OSC on {server.server_address}")

    server.serve_forever()

if __name__ == "__main__":
    main()
