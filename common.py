# Recovered from morinus.exe (Morinus 6.2, March 2014) by decompiling its Python 2.7
# bytecode; verified against the original bytecode. Original comments are not recoverable.
import os

class Common:

    def __init__(self):
        self.ephepath = os.path.join('SWEP', 'Ephem')
        self.symbols = os.path.join('Res', 'Morinus.ttf')
        self.abc = os.path.join('Res', 'FreeSans.ttf')
        self.signs = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l')
        self.planets = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')
        self.aspects = ('L', 'M', 'N', 'O', 'P', 'R', 'S')
        self.parallels = ('R', 'S')
        self.housenames = ('I', '2', '3', 'IV', '5', '6', 'VII', '8', '9', 'X', '11',
                           '12')
        self.housenames2 = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                            '12')
        self.fortune = 'J'
        self.retr = 'T'