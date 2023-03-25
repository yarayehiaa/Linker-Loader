import array 
from tkinter import *
from  tkinter import ttk
import re
import sys



n = input("Please enter whether your program is a SIC file or a SICXE file \n")
if(n=="sic"):
    import sicread
elif(n=="sicxe"):
    import gui_sic
else:
    print("Invalid choice \n")


