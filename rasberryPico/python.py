import machine
import utime

#Definovanie pinu pre LED (onboard LED na Raspberry Pi Pico W je na pinu 25)
led = machine.Pin("LED", machine.Pin.OUT)

#Blikanie LED
while True:
    led.value(1)
    print("LED je ZAPNUTÁ")
    utime.sleep_ms(1000)  # Počkajte 1 sekundu
    led.value(0)
    print("LED je Vypnuta")
    utime.sleep_ms(1000)