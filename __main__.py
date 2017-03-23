
import os
import sys
sys.path.append(os.path.dirname(__file__))

# from PySide.QtGui import QMainWindow

from thor import vector
if sys.version[0] == '3':
    try:
        from importlib import reload
    except:
        from imp import reload
reload(vector)


print("\n=============================")
print("TEST RUN STARTED.............")
print("=============================\n")

vector_a = vector.Vector4(1, 2, 3, 4)
print(vector_a)


print("VECTOR A . XYZW", vector_a.xyzw)
print("VECTOR A . XYZW", vector_a.wzyx)

print("\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
print("NORMALIZE.............")
print("/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n")

vector_a.normalize()
print("VECTOR A NORMALIZED", vector_a)
print("X", vector_a.x)
print("Y", vector_a.y)
print("Z", vector_a.z)
print("W", vector_a.w)
print("=+++++")

print('f', vector_a.xyz)
vector_a.rb = (1, 5)
vector_a.zx = (5, 5)
vector_a.y = 3.0
print("RBA", vector_a.rbag)


print("\n\n")
