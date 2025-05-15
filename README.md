# Para rodar o projeto no ESP32

Claro! Aqui está um **resumo direto e organizado** dos passos para rodar seu projeto de irrigação automática com ESP32, sensor de umidade e display LCD 16x2:

---

## ✅ RESUMO DOS PASSOS PARA RODAR O PROJETO

---

### 🔧 1. **Preparar o computador**

* Instale o **Python** no PC:
  👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

* Instale o **VS Code** ou **Thonny IDE**
  👉 [https://code.visualstudio.com/](https://code.visualstudio.com/)
  👉 [https://thonny.org/](https://thonny.org/)

* Instale os **drivers USB** da sua placa:

  * [CP2102 (ESP32 comum)](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
  * [CH340 (ESP8266)](https://sparks.gogo.co.nz/ch340.html)

---

### 🔥 2. **Gravar o firmware MicroPython no ESP32**

1. Baixe o firmware:
   👉 [https://micropython.org/download/esp32/](https://micropython.org/download/esp32/)

2. Instale o esptool:

   ```bash
   pip install esptool
   ```

3. Use o comando (substitua `COMx` e `firmware.bin`):

   ```bash
   esptool.py --chip esp32 --port COMx erase_flash
   esptool.py --chip esp32 --port COMx write_flash -z 0x1000 firmware.bin
   ```

---

### 📁 3. **Montar a estrutura do projeto**

Crie uma pasta com esses arquivos:

```
projeto_umidade/
│
├── main.py         ← Código principal
├── lcd_api.py      ← Biblioteca do LCD
└── i2c_lcd.py      ← Biblioteca do LCD
```

📥 Baixe as bibliotecas:

* `lcd_api.py`: [https://github.com/dhylands/python\_lcd/blob/master/lcd\_api.py](https://github.com/dhylands/python_lcd/blob/master/lcd_api.py)
* `i2c_lcd.py`: [https://github.com/dhylands/python\_lcd/blob/master/i2c\_lcd.py](https://github.com/dhylands/python_lcd/blob/master/i2c_lcd.py)

---

### 🛠️ 4. **Conectar os componentes**

| Componente            | ESP32         |
| --------------------- | ------------- |
| Sensor de Umidade     | GPIO 34 (ADC) |
| Relé (controle bomba) | GPIO 26       |
| LCD I2C SDA           | GPIO 21       |
| LCD I2C SCL           | GPIO 22       |

> Ligue também o **GND** e **VCC** corretamente (use 3.3V ou 5V conforme o módulo).

---

### 🧪 5. **Rodar o projeto**

**Usando o VS Code + Pymakr:**

* Instale a extensão **Pymakr**.
* Use “Upload Project to Device” para enviar os arquivos.
* Ou use Thonny e salve `main.py` na placa.

**Durante a execução:**

* Se umidade ≥ 74 → ativa o relé e exibe “REGANDO” no LCD.
* Se umidade < 74 → desliga o relé e mostra “PARADO”.

---

### 📝 Pronto!

Agora o projeto está funcionando:

* Monitora a umidade do solo.
* Liga/desliga a irrigação automaticamente.
* Mostra o status em tempo real no display.

Se quiser, posso te entregar um `.zip` pronto com os arquivos. Deseja isso?
