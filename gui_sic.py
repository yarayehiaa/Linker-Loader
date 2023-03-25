import array 
from tkinter import *
from  tkinter import ttk
import re
import sys


gadd=input("Enter starting address \n")
offset=gadd[4]
offset=int(offset,16)
gadd=int(gadd,16)
gadd1=gadd

newfile=open("systems test program.txt","r")
exsym=open("Ext_Sym_Table.txt","w")
progname=[]
proglen=[]
stradd=[]
tdictionary=[]
mdictionary=[]
rdictionary=[]
ddictionary={}
fullt=[]
fullm=[]
fullr=[]
fulld=[]
for x in newfile:
    if (x[0]=='H'):
        progname.append(x[1:7])
        stradd.append(x[7:13])
        proglen.append(x[13:21])  
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
            key=d[i]
            ddictionary.update({key:d[i+1]})
            #ddictionary.append(f)    
    elif(x[0]=="R"):
        r=re.findall('......',x[1:len(x)])
        rdictionary.append(r)
    elif(x[0]=="M"):
        madd=x[1:7]
        mlen=x[7:9]
        mrec=x[9:len(x)]
        m=[madd,mlen,mrec]
        mdictionary.append(m)
    elif(x[0]=="E"):
       fullt.append(tdictionary)
       fullm.append(mdictionary)
       fullr.append(rdictionary)
       fulld.append(ddictionary)
       tdictionary=[]
       mdictionary=[]
       rdictionary=[]
       ddictionary={}



for y in range(0,len(progname)):
    ddictionary=fulld[y]
    exsym.write(progname[y]+"\t\t"+'{:0>6X}'.format(gadd)+"\t"+proglen[y]) 
    stradd[y]=str(gadd)
    fulld.append({progname[y]:'{:0>6X}'.format(gadd)})
    tdictionary=fullt[y]
    for m in tdictionary:
        m[0]=int(m[0],16)+gadd
        m[0]='{:0>6X}'.format(m[0])
    for i ,(k,v)in enumerate(ddictionary.items()) :
        x=v
        x=int(x,16)
        x=x+gadd
        v='{:0>6X}'.format(x)
        ddictionary[k]=v
        exsym.write("\t"+k+"\t"+'{:0>6X}'.format(x)+"\n")
        
    mdictionary=fullm[y]  
    for h in mdictionary:
        h[0]=int(h[0],16)+gadd
        h[0]='{:0>6X}'.format(h[0])
    c=int(proglen[y],16)
    gadd=gadd+c
    
exsym.close()
#endadd=[]
prln=[]
printx=[]
for i in range(0,len(progname)):
    #endadd.append(stradd[i])+int(proglen[i],16)
    prln.append(int(proglen[i],16))
    prln[i]=prln[i]/0x10+1
    prln[i]=int(prln[i])
    printx1=[["00" for i in range(16)] for j in range(prln[i])] 
    printx.extend(printx1)

printable=[]

for i in range(0,len(progname)):
    tdictionary=fullt[i]
    ins=["00"]*16
    
    for x in tdictionary:
    
        
        row=x[0][3:6]
        row=int(row,16)/0x10
        row=int(row)-offset
        ins=printx[row]
        num=x[0]
        num=num[5]
        num=int(num,16)
        ins[num:]=x[2]
        while(len(ins)>16):
            newins=["00"]*16
            newins[0:]=ins[16:]
            ins=ins[0:16]
            #ins[num:16]=ins[num:16]
            printx[row]=ins
            ins=newins
            row=row+1
            printx[row]=ins
        if(len(ins)<16):
            s=len(ins)
            newins=["00"]*16
            ins[s:16]=newins[s:16]
            printx[row]=ins

        




printable=printx
res={}
for d in fulld:
    res.update(d)

for i in range(0,len(progname)):
    mdictionary=fullm[i]
    for x in mdictionary:
        x[2]=x[2][:-1]
        line=x[0]
        line=(int(line,16)-gadd1)
        line=line/0x10
        line=int(line)
        col=x[0][5]
        col=int(col,16)
        size=x[1]
        sign=x[2][0]
        x[2]=x[2][1:]
        op=res.get(x[2])
        if(sign=="+"):
            if(int(size)==6):
                
                if(col+2<=15):
                    z=printable[line][col]+printable[line][col+1]+printable[line][col+2]
                    op=int(z,16)+int(op,16)
                    op='{:06X}'.format(op & 0xFFFFFF)
                    printable[line][col]=op[0:2]
                    printable[line][col+1]=op[2:4]
                    printable[line][col+2]=op[4:6]
                if(col+2>15):
                    if(col==14):
                        z=printable[line][col]+printable[line][col+1]+printable[line+1][0]
                        op=int(z,16)+int(op,16)
                        op='{:0>6X}'.format(op)
                        printable[line][col]=op[0:2]
                        printable[line][col+1]=op[2:4]
                        printable[line+1][0]=op[4:6]
                    elif(col==15):
                        z=printable[line][col]+printable[line+1][0]+printable[line+1][1]
                        op=int(z,16)+int(op,16)
                        op='{:06X}'.format(op & 0xFFFFFF)
                        printable[line][col]=op[0:2]
                        printable[line+1][0]=op[2:4]
                        printable[line+1][1]=op[4:6]

            elif(int(size)==5):
                
                if(col+2<=15):
                    z=printable[line][col]+printable[line][col+1]+printable[line][col+2]
                    z=z[1:6]
                    op=int(z,16)+int(op,16)
                    op='{:06X}'.format(op & 0xFFFFFF)
                    cell=printable[line][col]
                    cell=cell[0:1]+op[1]
                    printable[line][col]=cell
                    printable[line][col+1]=op[2:4]
                    printable[line][col+2]=op[4:6]
                if(col+2>15):
                    if(col==14):
                        z=printable[line][col]+printable[line][col+1]+printable[line+1][0]
                        z=z[1:6]
                        op=int(z,16)+int(op,16)
                        op='{:06X}'.format(op & 0xFFFFFF)
                        cell=printable[line][col]
                        cell=cell[0:1]+op[1]
                        printable[line][col]=cell
                        printable[line][col+1]=op[2:4]
                        printable[line+1][0]=op[4:6]
                    elif(col==15):
                        z=printable[line][col]+printable[line+1][0]+printable[line+1][1]
                        z=z[1:6]
                        op=int(z,16)+int(op,16)
                        op='{:06X}'.format(op & 0xFFFFFF)
                        cell=printable[line][col]
                        cell=cell[0:1]+op[1]
                        printable[line][col]=cell
                        printable[line+1][0]=op[2:4]
                        printable[line+1][1]=op[4:6]
        elif(sign=="-"):
            if(int(size)==6):
                
                if(col+2<=15):
                    z=printable[line][col]+printable[line][col+1]+printable[line][col+2]
                    op=int(z,16)-int(op,16)
                    op='{:0>6X}'.format(op & 0xFFFFFF)
                    printable[line][col]=op[0:2]
                    printable[line][col+1]=op[2:4]
                    printable[line][col+2]=op[4:6]
                if(col+2>15):
                    if(col==14):
                        z=printable[line][col]+printable[line][col+1]+printable[line+1][0]
                        op=int(z,16)-int(op,16)
                        op='{:0>6X}'.format(op & 0xFFFFFF)
                        printable[line][col]=op[0:2]
                        printable[line][col+1]=op[2:4]
                        printable[line+1][0]=op[4:6]
                    elif(col==15):
                        z=printable[line][col]+printable[line+1][0]+printable[line+1][1]
                        op=int(z,16)-int(op,16)
                        op='{:0>6X}'.format(op & 0xFFFFFF)
                        printable[line][col]=op[0:2]
                        printable[line+1][0]=op[2:4]
                        printable[line+1][1]=op[4:6]

            elif(int(size)==5):
                
                if(col+2<=15):
                    z=printable[line][col]+printable[line][col+1]+printable[line][col+2]
                    z=z[1:6]
                    op=int(z,16)-int(op,16)
                    op='{:0>6X}'.format(op & 0xFFFFFF)
                    cell=printable[line][col]
                    cell=cell[0:1]+op[1]
                    printable[line][col]=cell
                    printable[line][col+1]=op[2:4]
                    printable[line][col+2]=op[4:6]
                if(col+2>15):
                    if(col==14):
                        z=printable[line][col]+printable[line][col+1]+printable[line+1][0]
                        z=z[1:6]
                        op=int(z,16)-int(op,16)
                        op='{:0>6X}'.format(op & 0xFFFFFF)
                        cell=printable[line][col]
                        cell=cell[0:1]+op[1]
                        printable[line][col]=cell
                        printable[line][col+1]=op[2:4]
                        printable[line+1][0]=op[4:6]
                    elif(col==15):
                        z=printable[line][col]+printable[line+1][0]+printable[line+1][1]
                        z=z[1:6]
                        op=int(z,16)-int(op,16)
                        op='{:0>6X}'.format(op & 0xFFFFFF)
                        cell=printable[line][col]
                        cell=cell[0:1]+op[1]
                        printable[line][col]=cell
                        printable[line+1][0]=op[2:4]
                        printable[line+1][1]=op[4:6]

ws  = Tk()
ws.title('linker Loader')
ws['bg'] = '#AC99F2'

game_frame = Frame(ws)
game_frame.pack()
game_scroll = Scrollbar(game_frame)
game_scroll.pack(side=RIGHT, fill=Y)

my_game = ttk.Treeview(game_frame,yscrollcommand=game_scroll.set)
my_game.pack()
game_scroll.config(command=my_game.yview)

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
 
gadd1=gadd1/0x10
gadd1=gadd1*0x10
#c=int(stradd,16)/0x10
#c=c*0x10
id=0

while(gadd1<gadd):
    
    my_game.insert(parent='',index='end',iid=id,text='',
    values=('{:04X}'.format(int(gadd1)),
    printable[id][0],printable[id][1],
    printable[id][2],printable[id][3],printable[id][4],printable[id][5],
    printable[id][6],printable[id][7],printable[id][8],printable[id][9],
    printable[id][10],printable[id][11],printable[id][12],printable[id][13],printable[id][14],printable[id][15]))
     
   

    id=id+1
    gadd1=gadd1+0x10
  









my_game.pack()

ws.mainloop()
