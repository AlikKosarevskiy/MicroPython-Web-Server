import machine
import socket
from machine import Pin, ADC
import time
# Set up analog pin
analog_pin = machine.ADC(Pin(1, mode=Pin.IN))

#LED
led = machine.Pin(15,machine.Pin.OUT)
for i in range(3):
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)


#led.off()

if led.value()==1:
        led_state ="ON"
if led.value()==0:
        led_state ="OFF"


# ************************
# Function for creating the
# web page to be displayed
def web_page():
    if led.value()==1:
        led_state = "ON"
        print('led is ON')
    elif led.value()==0:
        led_state = "OFF"
        print('led is OFF')

# Define HTML template with a placeholder for the analog value
html = """
HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>Pressure</title>
</head>
<body>
    <center><h2>ESP32 Web Server in MicroPython </h2></center>
    <center><h1>Analog Input: {analog_value}</h1></center>
        <center>   
         <form>   
          <button name="LED" type="submit" value="1" style="background-color: #4CAF50"> LED ON </button>   
          <button name="LED" type="submit" value="0" style="background-color: red"> LED OFF </button>   
         </form>   
 <center><p>LED is now <strong>{led_state}</strong>.</p></center>
 </body>
</html>
"""

# Set up socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 80))
s.listen(1)

# Loop forever
while True:
    # Wait for client to connect
    conn, addr = s.accept()
    print("Got connection from %s" % str(addr))
    
    # Socket receive()
    request=conn.recv(1024)
    print("")
    print("")
    print("Content %s" % str(request))
    # Read analog value
    analog_value = analog_pin.read()

 # Socket send()
    request = str(request)
    led_on = request.find('/?LED=1')
    led_off = request.find('/?LED=0')
    if led_on == 6:
        print('LED ON')
        print(str(led_on))
        led.value(1)
        led_state = "ON"
    elif led_off == 6:
        print('LED OFF')
        print(str(led_off))
        led.value(0)
        led_state = "OFF"
    response = web_page()


    # Send HTTP response with analog value in HTML template
    response = html.format(analog_value=analog_value, led_state=led_state)
    conn.send(response)

    # Close connection
    conn.close()