"""
This example combines both the debug window and the datasource as a poc 
"""

from X360DebugWindow import *
from X360DataSource import *

window = X360DebugWindow()
data_source = X360DataSource()

try:
    while True:
        try:
            data_packet = data_source.getLastPacket()
            window.view.updateViewWithPacket(data_packet)
        except AttributeError:
            pass
except KeyboardInterrupt:
    pass

