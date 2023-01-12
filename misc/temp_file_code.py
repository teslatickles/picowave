# # def start_socket(self) -> socket:
# #     addr = socket.getaddrinfo(self.LOCAL_IP, self.PORT)[0][-1]
# #     s = socket.socket()
# #     s.bind(addr)
# #     s.listen(1)
# #     print('listening on', addr)
# #     return s

# # async def serve_client(self, reader, writer):
# #     print('Client connected')
# #     request_line = await reader.readline()
# #     print("Request: {0}".format(request_line))

# #     while await reader.readline() != b"r\n":
# #         pass

# #     request = str(request_line)
# #     new_freq = request.find('/freq/update')
# #     new_duty = request.find('/duty-cycle/update')

# #     if self.new_freq_ok(new_freq):
# #         self.pwm.set_freq(new_freq)

# #     if self.new_duty_ok(new_duty):
# #         self.pwm.set_duty(new_duty)

# # form_cookie = '{freq}'.format(freq=new_freq)
# # form_cookie = '{dutycycle}'.format(dutycycle=new_duty)
# # print(form_cookie)

# new_freq = request.form['frequency']

# if 'read' in request.form:
#     pwm.set_freq(new_freq)
#     message_cookie = 'Frequency has updated to this requested value: {updated_freq}'.format(
#         updated_freq=new_freq)
#     print(message_cookie)

# new_duty = request.form['duty-cycle']

# if 'read' in request.form:
#     pwm.set_duty(new_duty)
#     message_cookie = 'Duty Cycle has updated to this requested value: {updated_duty_cycle}'.format(
#         updated_duty_cycle=new_duty)
#     print(message_cookie)


# // var p = freqValueForm.value / 1000; // period
#     // var o = p / 2; // oscillation
#     // var fps = 60;
#     // var n = 0;