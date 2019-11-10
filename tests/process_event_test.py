import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

import easysdl2 as esdl

esdl.init()
esdl.create_window()
while esdl.process_events():
    pass
esdl.quit()
