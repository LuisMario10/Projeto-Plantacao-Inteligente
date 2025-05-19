from machine import ADC, Pin
from time import sleep
from esp32_lcd import Esp32Lcd

# LCD 16x2 - pinos ligados ao ESP32
lcd = Esp32Lcd(
    rs=14,
    enable=27,
    d4=16,
    d5=17,
    d6=18,
    d7=19,
    num_lines=2,
    num_columns=16
)

# Sensor de umidade
moisture_sensor = ADC(Pin(34))
moisture_sensor.atten(ADC.ATTN_11DB)
moisture_sensor.width(ADC.WIDTH_10BIT)

# Relé de irrigação
relay = Pin(26, Pin.OUT)
relay.value(0)

def read_moisture():
    raw = moisture_sensor.read()
    moisture = (1023 - raw) * 100 // 1023
    return moisture

while True:
    moisture = read_moisture()
    print("Moisture: {}%".format(moisture))

    lcd.clear()
    lcd.putstr("Moisture: {}%".format(moisture))
    
    if moisture < 40:
        relay.value(1)
        lcd.move_to(0, 1)
        lcd.putstr("Watering ON")
    else:
        relay.value(0)
        lcd.move_to(0, 1)
        lcd.putstr("Watering OFF")

    sleep(2)
