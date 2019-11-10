import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

import easysdl2 as esdl

esdl.functions.init()
esdl.create_window()

font = esdl.Font("./fonts/VL-Gothic-Regular.ttf", 30)
solid = font.get_texture("Solid_Texture")
shaded = font.get_texture("Shaded_Texture", (255, 0, 255), esdl.Font.SHADED, (255, 255, 0))
blended = font.get_texture("Blended_Texture", (255, 0, 0), esdl.Font.BLENDED)

count = 0

while esdl.process_events():
    esdl.clear_screen()
    solid.draw(0, 0)
    shaded.draw(0, 40)
    blended.draw(0, 80)
    font.draw(0, 200, "count:{}".format(count), (255, 255, 0, 255), esdl.Font.BLENDED)
    esdl.update_screen()
    count += 1

esdl.quit()
