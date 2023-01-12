# use upip to install modules outside MicroPython
import pystone_lowmem
import network
import time
# import mip
# mip.install("micropython-pystone_lowmem")
pystone_lowmem.main()


class skynetNetwork:
    def __init__(self, pwm, ip: str = "192.168.50.2", port: int = 80) -> network.WLAN:
        self.LOCAL_IP = ip
        self.PORT = port

        self.pwm = pwm

        ssid = 'skynet'
        pwd = 'HunterH1'

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        # power mode ?
        wlan.config(pm=0xa11140)
        wlan.connect(ssid, pwd)
        print(wlan.ifconfig()[0])

        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break

            max_wait -= 1
            print('waiting for connection')
            time.sleep(1)
            print('.')

            if wlan.status() != 3:
                raise RuntimeError('network connection failed')
            else:
                status = wlan.ifconfig()
                print('Ready -- connected @ ip: {0}'.format(status[0]))
                break

        # return wlan
