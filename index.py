from machine import Pin, ADC, I2C
from time import sleep
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

moisture_sensor = ADC(Pin(34))
moisture_sensor.atten(ADC.ATTN_11DB)
moisture_sensor.width(ADC.WIDTH_10BIT)

relay = Pin(26, Pin.OUT)
relay.value(0)

i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

def read_moisture():
    value = moisture_sensor.read()
    moisture = (1023 - value) * 100 // 1023
    return moisture

while True:
    moisture = read_moisture()
    print("Moisture: {}%".format(moisture))

    if moisture >= 74:
        relay.value(1)
        lcd.clear()
        lcd.putstr("Status: WATERING")
    else:
        relay.value(0)
        lcd.clear()
        lcd.putstr("Status: STOPPED")

    sleep(2)

