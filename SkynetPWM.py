from machine import Pin, PWM
import time
# import logicanalyzer


class skynetPWM:
    def __init__(self, pin=15, inv_pin=16):
        super().__init__()

        # init pwm pins
        self.pwm_pin = PWM(Pin(pin))
        self.pwm_inv_pin = PWM(Pin(inv_pin))
        time.sleep(2)

        # init previous value holders
        self.prev_freq: float = 0
        self.prev_duty: float = 0

        # track state of output
        self.is_running = False

        # 10kHz
        self.INIT_FREQ = 10000

        # 50% duty cycle @ 500
        self.INIT_DUTY = 500

        # Init waveform generation
        # Active output at pins
        self.set_freq(self.INIT_FREQ)
        time.sleep(2)
        self.set_duty()
        time.sleep(2)

        # logicanalyzer.logic_analyzer_start()

    def new_freq_ok(self, new_freq: float) -> bool:
        self.prev_freq = self.pwm_pin.freq()
        return self.prev_freq != 0 and new_freq != 0 and self.prev_freq != None and new_freq != None and self.prev_freq != new_freq

    def new_duty_ok(self, new_duty: float) -> bool:
        self.prev_duty = self.pwm_pin.duty_u16()
        return self.prev_duty != 0 and new_duty != 0 and self.prev_duty != None and new_duty != None and self.prev_duty != new_duty

    def set_freq(self, new_freq: float) -> bool:
        if self.new_freq_ok(new_freq):
            self.pwm_pin.freq(new_freq)
            self.pwm_inv_pin.freq(new_freq)

    def get_freq(self) -> list:
        temp_list = list()
        temp_list.append(self.pwm_pin.freq())
        temp_list.append(self.pwm_inv_pin.freq())
        return temp_list

    # override built-in duty_u16 call
    # in order to set more easily
    def duty(self, d):
        if d is None:
            self.pwm_pin.duty_u16()
        if self.new_duty_ok(d):
            ddd = 65535*d//1000
            self.pwm_pin.duty_u16(ddd)
            self.pwm_inv_pin.duty_u16(ddd)

    # this starts waveform generation
    def set_duty(self, duty=500):
        self.current_duty = duty
        self.duty(duty)

    def get_duty(self) -> list(float):
        temp_list = list(float)
        temp_list.append(self.pwm_pin.duty(), self.pwm_inv_pin.duty())
        return temp_list

    def start(self, duty: float) -> bool:
        self.set_duty()
        self.is_running = True
        print('Generator started...')
        return 1

    def stop(self) -> bool:
        self.set_freq(0)
        self.set_duty(0)
        self.is_running = False
        print('Generator stopped')
        return 1

    def cleanup(self) -> bool:
        self.stop()
        self.pwm_pin.deinit()
        print(
            'De-initialized and cleaned up PWM Pin: {0}'.format(self.pwn_pin))
        return 1

    def log_pwm_setup_result(self, verbose: bool):
        if verbose:
            print('PWM Pins set:\nQ -> {0} @ {1}\nInverse -> {2} @ {3}'.format(
                self.pwm_pin, self.pwm_pin.freq(), self.pwm_inv_pin, self.pwm_inv_pin.freq()))
        else:
            print('PWM setup finished.')
