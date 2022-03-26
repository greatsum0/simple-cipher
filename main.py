from cipher import Cipher
import numpy as np
import re

f = open("table.txt", "r")
txt = f.read()
matrix = np.array(re.findall("[A-Z]+",txt))
matrix = matrix.reshape((26,26))

alice = Cipher("COBAIN",matrix)

bob = Cipher("COBAIN",matrix)

print(alice.encrypt("COME AS YOU ARE"))

print(bob.decrypt(alice.encrypt("COME AS YOU ARE")))

