# coding: utf-8

import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

from easysdl2 import *
from sdl2 import *

init()
create_window()
set_num_channel(10)
sound1 = Sound("sounds/sound1.wav")
sound2 = Sound("sounds/sound2.ogg")
while process_events():
    if check_key(SDLK_ESCAPE):
        break
    if check_key(SDLK_1):
        sound1.play(channel=0, loops=-1)
    if check_key(SDLK_2):
        sound2.play(channel=1, loops=-1)
    if check_key(SDLK_0):
        stop_all_sounds()
    clear_screen()
    fps.wait(10)
    update_screen()
del sound1
quit()
