import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

class LCDDisplay:
    ''' Class for LCD Display '''
    RST = None
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0

    def __init__(self):
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST)
        # Initialize library
        self.disp.begin()
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))
        self.padding = -2
        self.spacing = 13
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(
        "./usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size=12)
        #Clear Screen
        self.clear_display()

    def clear_display(self):
        self.disp.clear()
        self.disp.display()
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

    def write_lines(self, line: list, text: list):
        # Draw blank rectangle
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        for l, txt in zip(line, text):
            self.draw.text((0, l*self.spacing), txt, font=self.font, fill=255)

        self.disp.image(self.image)
        self.disp.display()

    def write_line(self, line, text):
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.draw.text((0, line*self.spacing), text, font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def example(self):
        self.draw.text((0, 0), "HEY BITCH", font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

if __name__ == "__main__":
    lcd = LCDDisplay()
    lcd.write_lines([0,1,2],["hello", "cunt", "slut"])
    #lcd.example()
