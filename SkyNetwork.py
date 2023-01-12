# use upip to install modules outside MicroPython
import pystone_lowmem
import network
import secrets
import time

# pystone_lowmem can be installed via Thonny
# or
# import mip
# mip.install("micropython-pystone_lowmem")

# need this either way
pystone_lowmem.main()


class skynetNetwork:
    def __init__(self, pwm) -> network.WLAN:
        self.pwm = pwm

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        # prevent default low-power mode
        self.wlan.config(pm=0xa11140)
        self.wlan.connect(secrets.SSID, secrets.PWD)
        time.sleep(1.5)

        self.conn_status = 'Connected'

        self.rp2040_ip = self.wlan.ifconfig()[0]
        print(self.rp2040_ip)
        print(self.wlan.ifconfig()[1])

        self.wlan_status = self.wlan.status()

        max_wait = 10
        while max_wait > 0:
            if self.wlan_status < 0 or self.wlan_status >= 3:
                break

            max_wait -= 1
            print('waiting for connection')
            time.sleep(1)
            print('.')

            if self.wlan_status != 3:
                self.conn_status = 'Disconnected'
                raise RuntimeError('network connection failed')
            else:
                self.conn_status = 'Connected'
                print('Ready -- connected @ ip: {0}'.format(self.rp2040_ip))
                break
