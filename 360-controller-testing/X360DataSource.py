"""
A very crude data source from a physical 360 controller, using the inputs library: https://github.com/zeth/inputs
Only supports both thumbsticks and triggers at the moment
Thumbstick values can range from -1 to 1, trigger values can range from 0 to 1
The raw values for these buttons range from -32768 to 32768 and 0 to 255
"""

import threading
import inputs

class X360DataSource(threading.Thread): 
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

        self.current_packet = {
            'LTS': {
                'X': 0,
                'Y': 0
            },
            'RTS': {
                'X': 0,
                'Y': 0
            },
            'TRG': {
                'L': 0,
                'R': 0
            }
        }

        self.last_packet = self.current_packet

        self.running = True

        self.start()

    def getLastPacket(self):
        return self.last_packet

    def run(self):
        while self.running:
            events = inputs.get_gamepad()

            for event in events:
                if event.ev_type == 'Absolute':
                    lts_val = event.state/32768
                    trg_val = event.state/255

                    if event.code == 'ABS_X':
                        self.current_packet['LTS']['X'] = lts_val
                    elif event.code == 'ABS_Y':
                        self.current_packet['LTS']['Y'] = lts_val
                    elif event.code == 'ABS_Z':
                        self.current_packet['TRG']['L'] = trg_val
                    elif event.code == 'ABS_RX':
                        self.current_packet['RTS']['X'] = lts_val
                    elif event.code == 'ABS_RY':
                        self.current_packet['RTS']['Y'] = lts_val
                    elif event.code == 'ABS_RZ':
                        self.current_packet['TRG']['R'] = trg_val
                    else:
                        print('Unimplemented control event', event.code, event.state)
                elif event.ev_type == 'Key':
                    print('Button press', event.code, event.state)
                elif event.ev_type == 'Sync':
                    if event.code == 'SYN_REPORT':
                        # print(current_packet)
                        self.last_packet = self.current_packet
                    else:
                        print('Unimplemented sync event', event.code, event.state)
                else:
                    print('Unimplemented event', event.ev_type, event.code, event.state)
