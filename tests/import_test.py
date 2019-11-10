import os
import sys

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

import easysdl2

easysdl2.set_log_file("test.log")
easysdl2.init()
easysdl2.quit()
