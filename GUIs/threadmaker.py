from threading import RLock
import sys
import GUI
sys.path.append("..")
from py2uart import UART

"""basically have a RLock that will have a dictionary that
    will be swapped by the GUI and the uart logger"""

