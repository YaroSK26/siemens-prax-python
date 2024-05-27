import network
import socket
import machine

wlan = network.WLAN(network.STA_IF)
ip = wlan.ifconfig()[0]
print(f'Pico W IP address: {ip}')

# Setup LED
led = machine.Pin(0, machine.Pin.OUT)

# HTML for the web page
html = """<!DOCTYPE html>
<html>
<head>
    <title>Pico W LED Control</title>
</head>
<body>
    <h1>LED Control</h1>
    <button onclick="fetch('/on')">Turn On</button>
    <button onclick="fetch('/off')">Turn Off</button>
</body>
</html>
"""

# Setup web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# Handle incoming connections
while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024).decode('utf-8')
    print('Request:', request)

    # Control LED based on request
    if 'GET /on' in request:
        led.value(1)  # Turn on the LED
    elif 'GET /off' in request:
        led.value(0)  # Turn off the LED

    # Send HTML response
    response = html
    cl.send('HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()