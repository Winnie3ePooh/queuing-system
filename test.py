import numpy as np
import random
import operator
import matplotlib.pyplot as plt

from math import log
from operator import add, truediv
from decimal import *

def generator(n,nu,seed):
    Y = []
    X = []
    a =  630360016
    m = 2**31-1
    Y0 = seed
    for i in range(0,n):
        Y.append((a*Y0)%m)
        Y0 = Y[-1]
        X.append(-nu*log(Y[-1]/m))
    return X

def priority(n,Xi,Pi,seed):
    bX = []
    a =  630360016
    m = 2**31-1
    X0 = seed
    for i in range(0,n):
        bX.append((a*X0)%m)
        X0 = bX[-1]
        bX[-1] = bX[-1]/m
    m = len(Xi)
    Y = [0]
    X = []
    for i in range(0,m):
        Y.append(round(Y[i]+Pi[i],1))
    for i in range(0,n):
        for j in range(0,m):
            if bX[i] > Y[j] and bX[i] <= Y[j+1]:
                X.append(Xi[j])
                break
    return X

class Requirement:
    def __init__(self,timeOne, timeTwo, timeThree, pType, rTime):
        self.arrivalTime = timeOne
        self.startTime = timeTwo
        self.endingTime = timeThree
        self.priority = pType
        self.remainingTime = rTime
    def set_par(self,timeTwo = None,
                timeThree = None, rTime = None):
        self.startTime = timeTwo
        self.endingTime = timeThree
        self.remainingTime = rTime


class Server:
    def __init__(self,S_LIMIT):
        self.__busy = []
        self.__time = 0
    def getStatus(self):
        return len(self.__busy)
    def setStatus(self, busy):
        self.__busy.append(busy)
    def getElem(self, index):
        return self.__busy.pop(index)
    def getTime(self,req):
        return self.__time
    def endIt(self,sT):
        index = next((i for i, item in enumerate(self.__busy) if item.endingTime == sT), -1)
        poped = self.__busy.pop(index)
        self.setStats(poped,sT)
    def setStats(self,pp,sT):
        self.__time += sT-pp.startTime
    def getStatistics(self,sT,S_LIMIT):
        if sT > 0:
            return self.__time/(sT*S_LIMIT)
        else:
            return 0
    def findMinPrior(self,prior):
        index = -1
        for k in range(1,prior):
            index = next((i for i, item in enumerate(self.__busy) if item.priority == k), -1)
            if index != -1:
                break
        return index

def checkServers(sT, qu, srvr,Y,eQ,eT,S_LIMIT):
    if qu:
        qu.sort(key=lambda x: x.priority, reverse=True)
    while (srvr.getStatus() < S_LIMIT) and qu:
        req = qu.pop(0)
        if req.remainingTime == None:
            endingTime = sT + Y.pop(0)
        else:
            endingTime = sT + req.remainingTime
        req.set_par(sT,endingTime)
        srvr.setStatus(req)
        eQ.append(endingTime)
        eT.append('E')

def swapDemands(cReq,srvr,index,sT,eQ,eT,qu,Y):
    req = srvr.getElem(index)
    eT.pop(eQ.index(req.endingTime))
    eQ.pop(eQ.index(req.endingTime))
    srvr.setStats(req,sT)
    req.remainingTime = sT - req.startTime
    req.endingTime = None
    req.startTime = None
    qu.insert(0,req)
    endingTime = sT + Y.pop(0)
    eQ.append(endingTime)
    eT.append('E')
    cReq.endingTime = endingTime
    cReq.startTime = sT
    srvr.setStatus(cReq)


#-------------------------------------------------------------------------------

def doABarrelRoll(N,NU_A,NU_S,LIMIT,S_LIMIT,pP,cP,SEED_A,SEED_S,LOOPS):
    #f = open('proverka'+str(g)+'.txt', 'w')
    #f = open('TEST.txt', 'w')
    p,Ns,Nq,Tq,Ts,Ca,Cr = 0,0,0,0,0,0,0

    for i in range(0,LOOPS):
        D_S,D_Q,A_D_S,A_D_Q,P_S,YY = [],[],[],[],[],[]
        sysTime = 0
        lastSysTime = 0
        sysEvent = ''
        queue = []
        eventQueue = []
        eventTypes = []
        SEED_A = random.randint(0,2**31-2)
        SEED_S = random.randint(0,2**31-2)
        X = generator(N,NU_A,SEED_A)
        #X = list(np.random.exponential(NU_A,N))
        Y = generator(N,NU_S,SEED_S)
        #Y = list(np.random.exponential(NU_S,N))
        sd = random.randint(1,2**31-2)
        #np.random.seed(sd)
        #P = list(np.random.choice(pP,N,p=cP))
        P = priority(N,pP,cP,sd)
        server = Server(S_LIMIT)
        d = 0
        Demands = 0
        N_S = 0
        while X:
            if queue:
                queue.sort(key=lambda x: x.priority, reverse=True)
            d += len(queue)*(sysTime-lastSysTime)
            if sysTime == 0:
                endingTime = sysTime + Y.pop(0)
                nextArrival = sysTime + X.pop(0)
                eventQueue.append(nextArrival)
                eventTypes.append('A')
                eventQueue.append(endingTime)
                eventTypes.append('E')
                req = Requirement(sysTime,sysTime,endingTime,P.pop(0),None)
                server.setStatus(req)
                Demands += 1

            if sysEvent == 'A':
                nextArrival = sysTime + X.pop(0)
                eventQueue.append(nextArrival)
                eventTypes.append('A')
                if server.getStatus() < S_LIMIT:
                    endingTime = sysTime + Y.pop(0)
                    eventQueue.append(endingTime)
                    eventTypes.append('E')
                    req = Requirement(sysTime,sysTime,endingTime,P.pop(0),None)
                    server.setStatus(req)
                    Demands += 1
                else:
                    if P[0] != 1:
                        if len(queue) < LIMIT:
                            check = server.findMinPrior(P[0])
                            if check != -1:
                                req = Requirement(sysTime,None,None,P.pop(0),None)
                                swapDemands(req,server,check,sysTime,eventQueue,eventTypes,queue,Y)
                                Demands += 1
                            else:
                                req = Requirement(sysTime,None,None,P.pop(0),None)
                                queue.append(req)
                                Demands += 1
                        else:
                            queue.pop()
                            check = server.findMinPrior(P[0])
                            if check != -1:
                                req = Requirement(sysTime,None,None,P.pop(0),None)
                                swapDemands(req,server,check,sysTime,eventQueue,eventTypes,queue,Y)
                                Demands += 1
                            else:
                                req = Requirement(sysTime,None,None,P.pop(0),None)
                                queue.append(req)
                                Demands += 1
                    else:
                        if len(queue) < LIMIT:
                            req = Requirement(sysTime,None,None,P.pop(0),None)
                            queue.append(req)
                            Demands += 1
                        else:
                            pass

            elif sysEvent == 'E':
                N_S += 1
                server.endIt(sysTime)

            checkServers(sysTime,queue,server,Y,eventQueue,eventTypes,S_LIMIT)

            YY.append(sysTime)
            D_S.append(server.getStatus()+len(queue))
            D_Q.append(len(queue))
            A_D_Q.append(d/(Demands*NU_A))
            A_D_S.append((NU_S+d/Demands)/NU_A)
            P_S.append(server.getStatistics(sysTime,S_LIMIT))

            forPop = np.argmin([eventQueue])
            lastSysTime = sysTime
            sysTime = eventQueue.pop(forPop)
            sysEvent = eventTypes.pop(forPop)

        p += P_S[-1]
        Ns += (NU_S+d/Demands)/NU_A
        Nq += d/(Demands*NU_A)
        Tq += d/Demands
        Ts += NU_S+d/Demands
        Ca += N_S/sysTime
        Cr += N_S/Demands

    return [YY,P_S,D_Q,D_S,A_D_S,A_D_Q] , [p/LOOPS,Tq/LOOPS,Ts/LOOPS,Nq/LOOPS,Ns/LOOPS,Ca/LOOPS,Cr/LOOPS]


if __name__ == "__main__":
    N=2000
    NU_A = 60
    NU_S = 180
    LIMIT = 14
    S_LIMIT = 6
    pP = [1,2,3]
    cP = [0.7,0.2,0.1]
    loops = 73
    asd, psd = doABarrelRoll(N,NU_A,NU_S,LIMIT,S_LIMIT,pP,cP,1235,2345,50)
    print('КОЭФФИЦИЕНТ ИСПОЛЬЗОВАНИЯ СИСТЕМЫ: {}'.format(psd[0]))
    print('СРЕДНЕЕ ВРЕМЯ В ОЧЕРЕДИ: {}'.format(psd[1]))
    print('СРЕДНЕЕ ВРЕМЯ В СИСТЕМЕ: {}'.format(psd[2]))
    print('СРЕДНЕЕ ПО ВРЕМЕНИ ЧИСЛО ТРЕБОВАНИЙ В ОЧЕРЕДИ: {}'.format(psd[3]))
    print('СРЕДНЕЕ ПО ВРЕМЕНИ ЧИСЛО ТРЕБОВАНИЙ В СИСТЕМЕ: {}'.format(psd[4]))
    print('АБСОЛЮТНАЯ ПРОПУСКНАЯ СПОСОБНОСТЬ: {}'.format(psd[5]))
    print('ОТНОСИТЕЛЬНАЯ ПРОПУСКНАЯ СПОСОБНОСТЬ: {}'.format(psd[6]))