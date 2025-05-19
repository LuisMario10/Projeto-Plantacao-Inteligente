from lcd_api import LcdApi
from machine import Pin
from time import sleep_us, sleep_ms

class Esp32Lcd(LcdApi):
    def __init__(self, rs, enable, d4, d5, d6, d7, num_lines=2, num_columns=16):
        self.rs = Pin(rs, Pin.OUT)
        self.enable = Pin(enable, Pin.OUT)
        self.data_pins = [Pin(d, Pin.OUT) for d in (d4, d5, d6, d7)]
        sleep_ms(20)
        self.rs.value(0)
        self._write_nibble(0x03)
        sleep_ms(5)
        self._write_nibble(0x03)
        sleep_us(200)
        self._write_nibble(0x03)
        self._write_nibble(0x02)  # 4-bit mode
        LcdApi.__init__(self, num_lines, num_columns)
        self.clear()
        self.hide_cursor()

    def _write_nibble(self, nibble):
        for i in range(4):
            self.data_pins[i].value((nibble >> i) & 1)
        self.enable.value(1)
        sleep_us(1)
        self.enable.value(0)
        sleep_us(100)

    def hal_write_command(self, cmd):
        self.rs.value(0)
        self._write_nibble(cmd >> 4)
        self._write_nibble(cmd & 0x0F)
        if cmd <= 3:
            sleep_ms(5)

    def hal_write_data(self, data):
        self.rs.value(1)
        self._write_nibble(data >> 4)
        self._write_nibble(data & 0x0F)

    def hal_sleep_us(self, usecs):
        sleep_us(usecs)

    def hal_backlight_on(self): pass
    def hal_backlight_off(self): pass
