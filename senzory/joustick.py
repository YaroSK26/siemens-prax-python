from machine import ADC, Pin
import time

vrx_pin = ADC(Pin(26))  
vry_pin = ADC(Pin(27))  

def read_joystick():
    x_value = vrx_pin.read_u16()  
    y_value = vry_pin.read_u16()  
    
    x_value_scaled = x_value >> 6  
    y_value_scaled = y_value >> 6  
    
    return x_value_scaled, y_value_scaled

while True:
    x, y = read_joystick()
    print("X:", x, "Y:", y)
    time.sleep(0.1) 



#Arduino Joystick pri zapojeni do Raspberry Pico W a pri spusteni tohto kodu ukazoval X Y suradnice Joysticku.