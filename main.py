import board
from adafruit_ina219 import INA219
from displayio import OnDiskBitmap, TileGrid, Group
import terminalio
import random
import time
from adafruit_display_text import bitmap_label
from adafruit_imageload import load

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
ina219 = INA219(i2c_bus)

main_group = Group()
board.DISPLAY.root_group = main_group

imgs = [f"/images/arrows/{x}.bmp" for x in range(1, 7)]

bitmap = OnDiskBitmap("/images/arrows/1.bmp")
tile_grid = TileGrid(bitmap=bitmap, pixel_shader=bitmap.pixel_shader)
tile_grid.x = (board.DISPLAY.width - bitmap.width) // 2
tile_grid.y = (board.DISPLAY.height - bitmap.height) // 2


text = "Engineering\nClub"
text_area = bitmap_label.Label(terminalio.FONT, text=text, scale=3, anchor_point=(0.5, 0.5), color=0x0b78e6)

text_area.anchored_position = (board.DISPLAY.width // 2, board.DISPLAY.height // 2)
main_group.append(text_area)
MAX_CURRENT = 40 #mA

time.sleep(1.5)
main_group.append(tile_grid)
main_group.remove(text_area)
main_group.append(text_area)

text_area.anchored_position = (board.DISPLAY.width // 2, board.DISPLAY.height - 12)
text_area.scale = 2

while True:
    bus_voltage = ina219.bus_voltage  # voltage on V- (load side)
    shunt_voltage = ina219.shunt_voltage  # voltage between V+ and V- across the shunt
    current = max(0, min(MAX_CURRENT, ina219.current))  # current in mA
    #print(current/MAX_CURRENT)     
    power = ina219.power  # power in watts
    blinka_img = None
    if (current/MAX_CURRENT <= 0.5):
        blinka_img = round(5*current/MAX_CURRENT*2)
        #main_group.rotation = 0
        tile_grid.flip_x = True
        tile_grid.flip_y = True
    else:
        blinka_img = round(5*2*(current/MAX_CURRENT-0.5))
        tile_grid.flip_x = False
        tile_grid.flip_y = False
    #print(imgs[blinka_img])
    bmp = OnDiskBitmap(imgs[blinka_img])
    tile_grid.bitmap = bmp
    tile_grid.pixel_shader = bmp.pixel_shader
    text_area.text = f"{round(current)} mA     {round(180-180*current/MAX_CURRENT)} dg"
    time.sleep(0.1)

