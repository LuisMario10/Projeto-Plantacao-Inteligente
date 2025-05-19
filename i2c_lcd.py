import time
import smbus
from .lcd_api import LcdApi

DEFAULT_I2C_ADDR = 0x27

MASK_RS = 0x01
MASK_RW = 0x02
MASK_E = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4

class I2cLcd(LcdApi):
    def __init__(self, port, i2c_addr, num_lines, num_columns):
        self.port = port
        self.i2c_addr = i2c_addr
        self.bus = smbus.SMBus(port)
        self.bus.write_byte(self.i2c_addr, 0)
        time.sleep(0.020)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.005)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.001)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.001)
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        time.sleep(0.001)
        LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA
        self.bus.write_byte(self.i2c_addr, byte | MASK_E)
        self.bus.write_byte(self.i2c_addr, byte)

    def hal_backlight_on(self):
        self.bus.write_byte(self.i2c_addr, 1 << SHIFT_BACKLIGHT)

    def hal_backlight_off(self):
        self.bus.write_byte(self.i2c_addr, 0)

    def hal_sleep_us(self, usecs):
        time.sleep(usecs / 1000000)

    def hal_write_command(self, cmd):
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                (((cmd >> 4) & 0x0f) << SHIFT_DATA))
        self.bus.write_byte(self.i2c_addr, byte | MASK_E)
        self.bus.write_byte(self.i2c_addr, byte)
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                ((cmd & 0x0f) << SHIFT_DATA))
        self.bus.write_byte(self.i2c_addr, byte | MASK_E)
        self.bus.write_byte(self.i2c_addr, byte)
        if cmd <= 3:
            time.sleep(0.005)

    def hal_write_data(self, data):
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                (((data >> 4) & 0x0f) << SHIFT_DATA))
        self.bus.write_byte(self.i2c_addr, byte | MASK_E)
        self.bus.write_byte(self.i2c_addr, byte)
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                ((data & 0x0f) << SHIFT_DATA))
        self.bus.write_byte(self.i2c_addr, byte | MASK_E)
        self.bus.write_byte(self.i2c_addr, byte)
