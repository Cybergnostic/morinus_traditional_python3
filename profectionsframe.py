# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import transitframe, common, mtexts, util

class ProfectionsFrame(transitframe.TransitFrame):

    def __init__(self, parent, title, chrt, radix, options):
        transitframe.TransitFrame.__init__(self, parent, title, chrt, radix, options)

    def change(self, chrt):
        self.chart = chrt
        self.w.chart = chrt
        self.w.drawBkg()
        self.w.Refresh()