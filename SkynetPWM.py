from machine import Pin, PWM
# import logicanalyzer


class skynetPWM:
    def __init__(self):
        super().__init__()
        self.pin = 15
        self.inv_pin = 16
        self.PWM_PIN_INDEX = 0
        self.PWM_INV_PIN_INDEX = 1

        # init prev value holders
        self.prev_freq: float = 0
        self.prev_duty: float = 0

        self.is_running = False

        # 10kHz
        self.INIT_FREQ = 10000
        # 50% duty cycle @ 500
        self.DUTY_CYCLE = 500

        self.pwm_pin = PWM(Pin(self.pin))
        self.pwm_inv_pin = PWM(Pin(self.inv_pin))

        # Init freq @ 10kHz
        self.set_freq(self.INIT_FREQ)
        # 50% duty cycle
        self.set_duty()

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
            super().duty_u16()
        if self.new_duty_ok(d):
            print(65535*d//1000)
            print(65535*d//100)
            super().duty_u16(65535*d//1000)

    # this starts waveform generation
    def set_duty(self, duty=500):
        self.duty(duty)
        # self.pwm_inv_pin.duty(self.DUTY_CYCLE)

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
