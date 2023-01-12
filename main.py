from machine import Pin, Timer
from microdot_asyncio import Microdot, send_file
from microdot_asyncio_websocket import with_websocket
import SkyNetwork as s_net
import SkynetPWM as s_pwm
import db_adapter as dba
import time

app = Microdot()
pwm = s_pwm.skynetPWM()
time.sleep(2)
pwm.log_pwm_setup_result(verbose=True)
net = s_net.skynetNetwork(pwm=pwm)
time.sleep(2)
fdb = dba.db_adapter()

# runtime status LED
led = Pin("LED", Pin.OUT)
led.value(0)
pwm.stop()
time.sleep(2)


@app.route('/')
def index(request):
    return send_file('index.html')


@app.route('/device/metadata')
@with_websocket
async def check_device_metadata(request, ws):
    conn_status = net.conn_status
    device_addr = net.rp2040_ip
    print(device_addr)
    device_port = '6343'

    a_ws_packet = '{conn_status}|{device_addr}|{device_port}'.format(
        conn_status=conn_status, device_addr=device_addr, device_port=device_port)
    print(a_ws_packet)

    # send the assembled packet
    await ws.send(a_ws_packet)


@app.route('/frequency/update')
@with_websocket
async def update_freq(request, ws):
    while True:
        new_freq = await ws.receive()
        new_freq = int(new_freq)
        pwm.set_freq(new_freq)


@app.route('/duty-cycle/update')
@with_websocket
async def update_duty_cycle(request, ws):
    while True:
        new_duty = await ws.receive()
        new_duty = int(new_duty)
        pwm.set_duty(new_duty)


@app.route('/utility')
@with_websocket
async def toggle_runtime(request, ws):
    while True:
        should_run = await ws.receive()
        if should_run == '1' and not pwm.is_running:
            pwm.start(pwm.current_duty)
            time.sleep(0.5)
            led.value(1)

        if should_run == '0' and pwm.is_running:
            pwm.stop()
            time.sleep(0.5)
            led.value(0)


@app.route('/save')
@with_websocket
async def save_parameters(request, ws):
    while True:
        param_packet = await ws.receive()
        # db.save_waveform_params(param_packet=param_packet)


app.run(debug=False)
