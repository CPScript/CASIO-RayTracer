import time # not fully required
import os # required
from os import system # required
from subprocess import call

print("Loading") # alert

time.sleep(1) # sleep
os.system('clear') # Might not work as this mainly works for 'unix' shells

print("Done, launching ray tracer") # alert that the 'clear' command worked
os.sysytem('clear')

print("""Depending on your calculator model this might crash your system and or worst might not work!
Raytracing software!""") # DISCLAIMER

time.sleep(5)
os.system('clear')


print("""



 \    /\
  )  ( ')
 (  /  )
  \(__)|
CASIO-RAYTRACER

------- BY-DISEASE/CPSscript --------

Would you like to run the ray tracer?
1 : YES
2 : QUIT

""") # banner
choice = input("Make Number Selection :")

if choice == "1":
    print("Loading...")
    call(["python", "r/main.py"])

if choice == "2":
    print("Process ending...")

exit
