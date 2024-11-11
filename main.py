import board
from adafruit_ina219 import INA219
from displayio import OnDiskBitmap, TileGrid, Group, Palette
import terminalio
import math
import time
import vectorio
from adafruit_display_text import bitmap_label
from adafruit_imageload import load

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
ina219 = INA219(i2c_bus)

main_group = Group()
board.DISPLAY.root_group = main_group

text = "Engineering\nClub"
text_area = bitmap_label.Label(terminalio.FONT, text=text, scale=3, anchor_point=(0.5, 0.5), color=0x0b78e6)

text_area.anchored_position = (board.DISPLAY.width // 2, board.DISPLAY.height // 2)
main_group.append(text_area)
def rotate_point(x, y, abtx, abty, angle):
    """
    Rotates a point (x, y) around the origin by a given angle (in radians).
    """
    og_angle = math.atan2(y-abty, x-abtx)
    hyp = math.sqrt((x-abtx)*(x-abtx) + (y-abty)*(y-abty))
    new = ((math.cos(og_angle+angle)*(hyp)+abtx), (math.sin(og_angle+angle)*(hyp)+abty))
    return new

def rotate_points(points, center, angle):
    """
    Rotates a list of points around the origin by a given angle (in radians).
    """
    rotated_points = []
    for (x, y) in points:
        rotated_points.append(rotate_point(x, y, center[0], center[1], angle))
    return rotated_points

path0_w = 25.107
path0_h = 127.418
points = [(18.483,125.866),(18.483,115.879),(18.483,105.862),(18.483,95.877),(18.484,85.879),(18.483,75.873),(18.483,65.865),(18.483,55.871),(20.626,47.149),(25.227,41.830),(22.968,32.081),(20.710,22.339),(18.452,12.595),(16.194,2.853),(11.148,5.861),(8.602,15.547),(6.063,25.207),(3.521,34.879),(0.976,44.560),(8.948,47.422),(9.917,57.077),(9.917,67.078),(9.917,77.083),(9.917,87.081),(9.917,97.079),(9.917,107.074),(9.917,117.068),(10.274,127.011),]

def flatten_points(point_list):
    return [(int(x[0]), int(x[1])) for x in point_list]

palette = Palette(1)
palette[0] = 0xFFFFFF
MAX_CURRENT = 50 #mA

polygon_shape = vectorio.Polygon(
        pixel_shader=palette,
        points=flatten_points(points),
        x=100, y=8
)
time.sleep(1.5)
main_group.append(polygon_shape)
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
    #rotated_points = rotate_points(points, (board.DISPLAY.width//2, board.DISPLAY.height//2), current/MAX_CURRENT*2*math.pi)
    # 11.5 on x and half of the display height on y is the center of the arrow
    rotated_points = rotate_points(points, (path0_w/2, path0_h/2), current/MAX_CURRENT*2*math.pi)
    polygon_shape.points = flatten_points(rotated_points)
    text_area.text = f"{round(current)} mA     {round(360*current/MAX_CURRENT)} dg"
    time.sleep(0.01)


