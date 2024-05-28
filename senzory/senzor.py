import network
import socket
import machine
import utime

# Initialize the rotary encoder pins
clk = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_DOWN)
dt = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Initialize counter
counter = 0
clk_last_state = clk.value()

# Function to handle rotary encoder changes
def rotary_interrupt_handler(pin):
    global counter, clk_last_state
    clk_state = clk.value()
    dt_state = dt.value()
    if clk_state != clk_last_state:
        if dt_state != clk_state:
            counter += 1
        else:
            counter -= 1
    clk_last_state = clk_state

# Attach interrupt handlers
clk.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=rotary_interrupt_handler)

# Setup Wi-Fi connection
wlan = network.WLAN(network.STA_IF)
ip = wlan.ifconfig()[0]
print(f'Pico W IP address: {ip}')

# HTML template for the web page
html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Pico W Rotary Encoder Counter</title>
</head>
<body>
    <h1>Rotary Encoder Counter</h1>
    <p>Counter Value: <span id="counter">{counter}</span></p>
    <script>
        var counterElement = document.getElementById('counter');

        // Function to update counter value
        function updateCounter() {{
            fetch('/counter')
                .then(response => response.text())
                .then(value => {{
                    counterElement.textContent = value;
                }});
        }}

        // Periodically update counter value
        setInterval(updateCounter, 1000);

        // Initial update
        updateCounter();
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

    # Get counter value
    if 'GET /counter' in request:
        cl.send('HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\n')
        cl.send(str(counter))
        cl.close()
        continue

    # Send HTML response with current counter value
    html_response = html_template.format(counter=counter)
    cl.send('HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(html_response)
    cl.close()