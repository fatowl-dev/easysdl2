# cofing: utf-8

import os
import sys
import time

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

import easysdl2

easysdl2.init()
easysdl2.create_window()
time.sleep(3)
easysdl2.quit()
