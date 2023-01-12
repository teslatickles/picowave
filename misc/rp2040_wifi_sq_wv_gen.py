# Main file for Square Wave Generator
# Calls setup functions for WiFi and hardware PWM
# runs async socket server

async def main():
    # init PWM
    pwm = s_pwm.skynetPWM(None, 16, 15)

    print(
        'PWM Pins set:\nQ -> {0} @ {1}\nInverse -> {2} @ {3}'.format(pwm[pwm.PWM_PIN_INDEX], pwm.get_freq()[pwm.PWM_PIN_INDEX], pwm[pwm.PWM_INV_PIN_INDEX], pwm.get_freq()[pwm.PWM_INV_PIN_INDEX]))

    # init and start websocket
    net = s_net.skynetNetwork(pwm)
    socket = net.start_socket()
    print('Websocket server starting - Details: {0}'.format(socket))

    asyncio.create_task(asyncio.start_server(
        net.serve_client, net.LOCAL_IP, net.PORT))
    print('Websocket server @ {0}:{1}'.format(net.LOCAL_IP, net.PORT))


if __name__ == '__main__':
    import SkyNetwork as s_net
    import SkynetPWM as s_pwm
    import asyncio

    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()
