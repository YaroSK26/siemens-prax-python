import network
import socket
import machine

wlan = network.WLAN(network.STA_IF)
ip = wlan.ifconfig()[0]
print(f'Pico W IP address: {ip}')

# Setup LED
led = machine.Pin(0, machine.Pin.OUT)

# Initialize LED status
led_status = False

# Function to turn LED on
def turn_on():
    global led_status
    led_status = True
    led.on()

# Function to turn LED off
def turn_off():
    global led_status
    led_status = False
    led.off()

# HTML for the web page
html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Pico W LED Control</title>
</head>
<body>
    <h1>LED Control</h1>
    <p>LED Status: <span id="status">{status}</span></p>
    <button onclick="fetch('/on')">Turn On</button>
    <button onclick="fetch('/off')">Turn Off</button>
    <script>
        var statusElement = document.getElementById('status');

        // Function to update LED status
        function updateStatus() {{
            fetch('/status')
                .then(response => response.text())
                .then(status => {{
                    statusElement.textContent = status;
                }});
        }}

        // Periodically update LED status
        setInterval(updateStatus, 1000);

        // Initial update
        updateStatus();
    </script>
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

    # Turn LED on
    if 'GET /on' in request:
        turn_on()

    # Turn LED off
    if 'GET /off' in request:
        turn_off()

    # Get LED status
    if 'GET /status' in request:
        status = 'ON' if led_status else 'OFF'
        cl.send('HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\n')
        cl.send(status)
        cl.close()
        continue

    # Send HTML response with LED status
    status_text = 'ON' if led_status else 'OFF'
    html_response = html_template.format(status=status_text)
    cl.send('HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(html_response)
    cl.close()