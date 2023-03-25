import array 
from tkinter import *
from  tkinter import ttk
import re

gadd=0x000000
newfile=open("sicxe1.txt","r")
exsym=open("Ext_Sym_Table.txt","w")
progname=''
proglen=0
stradd=0
tdictionary=[]
mdictionary=[]
rdictionary=[]
ddictionary=[]

for x in newfile:
    if (x[0]=='H'):
        progname=x[1:7]
        stradd=x[7:13]
        proglen=x[13:21]   
    elif(x[0]=='T'):
        tadd=x[1:7]
        tlen=x[7:9]
        trec=x[9:len(x)]
        trec=re.findall('..',trec)
        t=[tadd,tlen,trec]
        tdictionary.append(t)
    elif(x[0]=='D'):
        d=re.findall('......',x[1:len(x)])
        
        for i in range(0,len(d)-1,2):
            f=[d[i],d[i+1]]
            ddictionary.append(f)
            
        
    elif(x[0]=="R"):
        r=re.findall('......',x[1:len(x)])
        rdictionary.append(r)
    elif(x[0]=="M"):
        madd=x[1:7]
        mlen=x[7:9]
        mrec=x[9:len(x)]
        m=[madd,mlen,mrec]
        mdictionary.append(m)



exsym.write(progname+"\t\t"+'{:0>6X}'.format(gadd)+"\t"+proglen) 
for i in range(0,len(ddictionary)) :
    x=int(ddictionary[i][1],16)
    x=x+gadd
    exsym.write("\t"+ddictionary[i][0]+"\t"+'{:0>6X}'.format(x)+"\n")
exsym.close()

endadd=int(stradd,16)+int(proglen,16)
prln=int(proglen,16)
prln=prln/0x10+1
prln=int(prln)
printx=[["xx" for i in range(16)] for j in range(prln)] 
printable=[]

for x in tdictionary:
    
    ins=["xx"]*16
    row=int(x[0],16)/0x10
    row=int(row)
    num=x[0]
    num=num[5]
    num=int(num,16)
    ins[num:(len(x[2])+num)]=x[2]
    if(len(ins)>16):
        newins=["xx"]*16
        newins[0:(len(ins)-16)]=ins[16:len(ins)]
        ins=ins[0:16]
        printx[row]=ins
        ins=newins
        row=row+1
    
    printx[row]=ins




printable=printx


for x in mdictionary:
    x[2]=x[2][:-1]
    line=x[0]
    line=int(line,16)/0x10
    line=int(line)
    col=x[0][5]
    col=int(col,16)
    size=x[1]
    op=x[2]
    if(int(size)==6):
        printable[line][col]=op[0:2]
        printable[line][col+1]=op[2:4]
        printable[line][col+2]=op[4:6]
    elif(int(size)==5):
        cell=printable[line][col]
        cell=cell[0:1]+op[1]
        printable[line][col]=cell
        printable[line][col+1]=op[2:4]
        printable[line][col+2]=op[4:6]


ws  = Tk()
ws.title('linker Loader')
ws['bg'] = '#AC99F2'

game_frame = Frame(ws)
game_frame.pack()

my_game = ttk.Treeview(game_frame)

my_game['columns'] = ('Address','0', '1', '2', '3', '4','5','6','7','8','9','A','B','C','D','E','F')

my_game.column("#0", width=0,  stretch=NO)
my_game.column("Address",anchor=CENTER,width=80)
my_game.column("0",anchor=CENTER,width=80)
my_game.column("1",anchor=CENTER, width=80)
my_game.column("2",anchor=CENTER,width=80)
my_game.column("3",anchor=CENTER,width=80)
my_game.column("4",anchor=CENTER,width=80)
my_game.column("5",anchor=CENTER,width=80)
my_game.column("6",anchor=CENTER,width=80)
my_game.column("7",anchor=CENTER,width=80)
my_game.column("8",anchor=CENTER,width=80)
my_game.column("9",anchor=CENTER,width=80)
my_game.column("A",anchor=CENTER,width=80)
my_game.column("B",anchor=CENTER,width=80)
my_game.column("C",anchor=CENTER,width=80)
my_game.column("D",anchor=CENTER,width=80)
my_game.column("E",anchor=CENTER,width=80)
my_game.column("F",anchor=CENTER,width=80)


my_game.heading("#0",text="",anchor=CENTER)
my_game.heading("Address",text="Address",anchor=CENTER)
my_game.heading("0",text="0",anchor=CENTER)
my_game.heading("1",text="1",anchor=CENTER)
my_game.heading("2",text="2",anchor=CENTER)
my_game.heading("3",text="3",anchor=CENTER)
my_game.heading("4",text="4",anchor=CENTER)
my_game.heading("5",text="5",anchor=CENTER)
my_game.heading("6",text="6",anchor=CENTER)
my_game.heading("7",text="7",anchor=CENTER)
my_game.heading("8",text="8",anchor=CENTER)
my_game.heading("9",text="9",anchor=CENTER)
my_game.heading("A",text="A",anchor=CENTER)
my_game.heading("B",text="B",anchor=CENTER)
my_game.heading("C",text="C",anchor=CENTER)
my_game.heading("D",text="D",anchor=CENTER)
my_game.heading("E",text="E",anchor=CENTER)
my_game.heading("F",text="F",anchor=CENTER)
 
gadd=gadd/0x10
gadd=gadd*0x10
#c=int(stradd,16)/0x10
#c=c*0x10
id=0

while(gadd<endadd):
    
    my_game.insert(parent='',index='end',iid=id,text='',
    values=('{:04X}'.format(int(gadd)),
    printable[id][0],printable[id][1],
    printable[id][2],printable[id][3],printable[id][4],printable[id][5],
    printable[id][6],printable[id][7],printable[id][8],printable[id][9],
    printable[id][10],printable[id][11],printable[id][12],printable[id][13],printable[id][14],printable[id][15]))
     
   

    id=id+1
    gadd=gadd+0x10
  









my_game.pack()

ws.mainloop()
