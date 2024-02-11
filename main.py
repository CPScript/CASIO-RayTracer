import time # not fully required
import os # required
from os import system # required
from subprocess import call

def clear():
 os.system('cls' if os.name == 'nt' else 'clear')


print("Loading!!!") # alert
print("Done, launching ray-tracer") # alert that the 'clear' command worked
time.sleep(1)
clear()

print("""
Depending on your calculator model this might crash your system!
And or might not work on your calculator!
""") # DISCLAIMER

time.sleep(5)
clear()

print("""
-------------------------
| CASIO fx-CG RAYTRACER |
-------------------------
| BY - DISEASE/CPScript |
-------------------------
|
| Would you like to run the ray-tracer?
| 1 : YES
| 2 : QUIT
| """) # banner
choice = input("| Make Number Selection :")

if choice == "1":
    print("Loading...")
    clear()
    call(["python", "asset/ray.py"])

if choice == "2":
    clear()
    print("Process ending...")

exit
