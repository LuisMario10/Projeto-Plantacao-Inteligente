from machine import Pin, ADC, I2C
from time import sleep
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

# Configurações do sensor e relé
sensor_umidade = ADC(Pin(34))
sensor_umidade.atten(ADC.ATTN_11DB)  # Para permitir leitura até 3.6V
sensor_umidade.width(ADC.WIDTH_10BIT)  # Valor de 0 a 1023

rele = Pin(26, Pin.OUT)
rele.value(0)  # Inicialmente desligado

# Configuração do LCD via I2C
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # Endereço I2C pode variar (0x27 ou 0x3F)

# Função para mapear leitura (ajuste conforme calibração)
def ler_umidade():
    valor = sensor_umidade.read()
    umidade = (1023 - valor) * 100 // 1023  # Invertemos: solo seco = 0, molhado = 100
    return umidade

# Loop principal
while True:
    umidade = ler_umidade()
    print("Umidade: {}%".format(umidade))

    if umidade >= 74:
        rele.value(1)
        lcd.clear()
        lcd.putstr("Status: REGANDO")
    else:
        rele.value(0)
        lcd.clear()
        lcd.putstr("Status: PARADO")

    sleep(2)
