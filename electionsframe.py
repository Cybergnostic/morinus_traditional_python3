# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import transitframe
import common
import mtexts

class ElectionsFrame(transitframe.TransitFrame):

    def __init__(self, parent, title, chrt, radix, options):
        transitframe.TransitFrame.__init__(self, parent, title, chrt, radix, options)

    def change(self, chrt, title):
        self.chart = chrt
        self.w.chart = chrt
        self.w.drawBkg()
        self.w.Refresh()