import os
from os import listdir
from os.path import isfile, join


path = 'Data'
for f in listdir(path):
    if join(path, f).endswith('.txt'):
        file = join(path, f)
        name = os.path.splitext(file)[0]
        print(file)
        print(name)