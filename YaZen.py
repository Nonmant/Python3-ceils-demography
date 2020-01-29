from os import system, name as osName
import random
import time
import threading
import sys

def cls():
    system('cls' if osName=='nt' else 'clear')

def showState(fieldList):
    cls()
    print("Press Enter to stop")
    for line in fieldList:
        print(*line,sep="")

def listSlice2d(list, rowsRange, colsRange):
    return [row[colsRange[0]:colsRange[1]] for row in list[rowsRange[0]:rowsRange[1]]]

def listCopy2d(list):
    return [row[:] for row in list]

def showHelp():
    print("Arguments:",
              "-r 4 6  - 4x6 matrix with random fillment",
              "-f text.txt  - read from file",
              "\nText file template:",
              "3 2  -3x2 matrix",
              "10  - values\n11\n00",
              "\nPress Enter to run default",
              sep="\n")
    input()
 
class Updater(threading.Thread):  
    def __init__(self, field):
        self.field = field
        self.m=len(field)
        self.n=len(field[0])
        self.nextField = [[0]*n for i in range(m)]
        self.fieldNeighs = self.initFieldNeighs()
        self.stopFlag=False
        self.stableStateFlag=False
        self.count=0
        threading.Thread.__init__(self)

    def stop(self):
        self.stopFlag=True

    def countNeighbours(self, i,j):
        rangeRows=[max(i-1,0), min(i+1,self.m)+1]
        rangeCols=[max(j-1,0), min(j+1,self.n)+1]
        matr=listSlice2d(self.field, rangeRows, rangeCols)
        sum1=map(sum,matr)
        sumMatr=sum(sum1)
        return sumMatr-self.field[i][j]

    def incrementNeighbours(self,i1,j1,inc):
        if not inc:
            return
        rangeRows=[max(i1-1,0), min(i1+2,self.m)]
        rangeCols=[max(j1-1,0), min(j1+2,self.n)]
        for i in range(rangeRows[0],rangeRows[1]):
            for j in range(rangeCols[0],rangeCols[1]):
                self.fieldNeighs[i][j]+=inc
        self.fieldNeighs[i1][j1]-=inc

    def initFieldNeighs(self):
        fieldNeighs=[ [0] * n for i in range(m) ]
        for i in range(self.m):
            for j in range(self.n):
                fieldNeighs[i][j]=self.countNeighbours(i,j)
        return fieldNeighs

    def run(self):
        while (not time.sleep(1))and(not self.stopFlag):
            for i in range(self.m):
                for j in range(self.n):
                    num=self.fieldNeighs[i][j]
                    if self.field[i][j]==1:
                        self.nextField[i][j] = int(num in [2,3])
                    else:
                        self.nextField[i][j] = int(num == 3)
                    self.incrementNeighbours(i,j, self.nextField[i][j] - self.field[i][j])

            if self.field==self.nextField:
                self.stableStateFlag=True
                break

            self.field=listCopy2d(self.nextField)
            showState(self.field)
            self.count+=1
        showState(self.field)
        print("Stopped at step ", self.count, ("", ", stable state")[self.stableStateFlag], sep="")

args=sys.argv

flagFile=False
flagRand=False
flagDefault=True

ranGen=random.Random()

try:
    if(args[1]=="-f"):
        flagFile=True
    elif(args[1]=="-r"):
        flagRand=True
    elif(args[1]=="-h"):
        showHelp()
except:
    showHelp()

                
if flagFile:
    try:
        f = open(args[2], 'r')
        m,n=map(int, f.readline().split(" "))#m - rows, n - columns

        field=[[] for i in range(m)]
        for i in range(m):
            field[i]=list(map(int, list(f.readline().strip())))
            if(len(field[i])!=n):
                raise Exception
        f.close()
        del f
        flagDefault=False
    except:
        print("Sth bad with file", args[2])
        flagFile=False
        showHelp()
elif flagRand:
    try:
        m=int(args[2])
        n=int(args[3])
        flagDefault=False
    except:
        print("Sth wrong with rand params", args[2], args[3])
        flagRand=False
        showHelp()

if flagDefault:
    m=ranGen.randint(3,10)
    n=ranGen.randint(3,10)

if flagDefault or flagRand:   
    field=[[ranGen.randint(0,1) for j in range(n)] for i in range(m)]

del flagFile, flagRand, flagDefault, args, ranGen

upd=Updater(field)
upd.start()


input()
upd.stop()
upd.join()

