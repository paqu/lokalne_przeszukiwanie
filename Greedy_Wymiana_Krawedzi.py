import tsplib95
import numpy as np
import matplotlib.pyplot as plt 
import random as rd
import copy
import time########################
plik="kroB100"
liczbaPowtorzen=100
procentMiastDoOdwiedzenia=50
def podzialInt (linia):
    tab2=np.array                   #miejsce na linie na tabelke
    tab=[]
    #print(linia)
    for i in linia.split(" "):      #podzial
       try:
           tab.append(int(i))
       except ValueError:
            try:
                tab.append(float(i))
            except ValueError:
                return False
    tab2=tab

    return tab2
def WczytajProblem(sciezkaDoPliku):
    import tsplib95
    import numpy as np
    problem=tsplib95.load_problem(sciezkaDoPliku)
    lista=list(problem.get_edges())
    #problem.wfunc(1,2)
    tab=[]
    for x,y in lista:
        tab.append(problem.wfunc(x,y))
    tab2=np.array(tab)
    return tab2.reshape(x,y)

def ObliczLacznyKoszt(macierzOdleglosci, sciezkaRuchu):
    kosztLaczny=macierzOdleglosci[sciezkaRuchu[0],sciezkaRuchu[-1]]
    for i in range (len(sciezka)-1):
        kosztLaczny+=macierzOdleglosci[sciezkaRuchu[i],sciezkaRuchu[i+1]]
    return kosztLaczny

def RysujWykres(sciezkaDoPliku,sciezkaRuchu,kosztLaczny,startMiasto,opis):
    import pylab
    import matplotlib
    import matplotlib.pyplot as plt
    #Wykres
    f=open(sciezkaDoPliku,"r")
    tab=[]
    for linia in f:
        if podzialInt(linia)!=False:
            tab.append(podzialInt(linia))
    tab=np.array(tab)
    tab2=[]
    
    pylab.plot(tab[:,1],tab[:,2],'ko')#wszystkie
    #pylab.plot(tab[startMiasto,1],tab[startMiasto,2],'go')
    pylab.title(opis)
    for punkt in range(tab.shape[0]):
        pylab.annotate(tab[punkt,0]-1,xy=(tab[punkt,1]-80,tab[punkt,2]+50))
    for punkt in sciezkaRuchu:
        tab2.append(tab[punkt,:])
    tab2.append(tab[sciezka[0]])
    tab2=np.array(tab2)
    pylab.plot(tab2[:,1],tab2[:,2],'r')
    #pylab.plot(tab2[startMiasto,1],tab2[startMiasto,2],'g')
    #pylab.annotate("haha",xy=(2,2),xytext=(10,1000))
    pylab.show()
    print("Laczny koszt: ",kosztLaczny)
class Rozwiazanie():
    def __init__(self,sciezkaDoPliku,sciezkaRuchu,kosztLaczny,startMiasto,opis,duration):###########################
        self.duration=duration
        self.sciezkaDoPliku=sciezkaDoPliku
        self.sciezkaRuchu=sciezka
        self.kosztLaczny=kosztLaczny
        self.kosztLaczny=kosztLaczny
        self.startMiasto=startMiasto
        self.opis=opis
    def Koszt(self):
        return self.kosztLaczny
    def Czas(self):
        return self.duration############################################################
    def Rysuj(self):
        import pylab
        import matplotlib
        import matplotlib.pyplot as plt
        
        #Wykres
        f=open(self.sciezkaDoPliku,"r")
        tab=[]
        for linia in f:
            if podzialInt(linia)!=False:
                tab.append(podzialInt(linia))
        tab=np.array(tab)
        tab2=[]
        
        pylab.plot(tab[:,1],tab[:,2],'ko')#wszystkie
        #pylab.plot(tab[self.startMiasto,1],tab[self.startMiasto,2],'go')
        pylab.title(self.opis)
        for punkt in range(tab.shape[0]):
            pylab.annotate(tab[punkt,0]-1,xy=(tab[punkt,1]-80,tab[punkt,2]+50))
        for punkt in self.sciezkaRuchu:
            tab2.append(tab[punkt,:])
        tab2.append(tab[self.sciezkaRuchu[0]])
        tab2=np.array(tab2)
        pylab.plot(tab2[:,1],tab2[:,2],'r')
        #pylab.plot(tab2[startMiasto,1],tab2[startMiasto,2],'g')
        #pylab.annotate("haha",xy=(2,2),xytext=(10,1000))
        pylab.show()
def ciagLosowychCalkowitych(dlugosc,zakres):
    ciag=np.array(int(np.random.rand()*zakres))
    for i in range(dlugosc-1):
        losowa=int(np.random.rand()*zakres)
        while(np.sum((ciag==losowa).astype(int))!=0):
            losowa=int(np.random.rand()*zakres)
        ciag=np.append(ciag,losowa)
    return ciag

#plik="kroA100"
#liczbaPowtorzen=2
#procentMiastDoOdwiedzenia=50
zal=1
if plik==1:
    plik="kroA100"
elif plik==2:
    plik="kroB100"
sciezkaDoPliku="instances/"+plik+".tsp"
#sciezkaDoPliku="instances/kroA100.tsp"
zbiorRozwiazan=[]
for i in range(liczbaPowtorzen):
    startTime = time.time()#########################
    print("Powtorzenie: ",i)
    odleglosci=WczytajProblem(sciezkaDoPliku) #Zwraca macierz odleglosci miast
    odleglosciWzorzec=copy.deepcopy(odleglosci)#Wzorzec macierzy odleglosci
    #od teraz jest macierz odleglosci jako odleglosci. Wszystko leci od niej
    iloscMiast=odleglosci.shape[0]      #Określenie ilości miast 

    #startMiasto=rd.randint(0,iloscMiast-1)  #Określenie miasta startowego
    startMiasto=i                        #wybór ręczny miasta startowego
   
          #Utworzenie tabeli zachowującej ścieżkę
    sciezka=ciagLosowychCalkowitych(int(iloscMiast*procentMiastDoOdwiedzenia/100),iloscMiast)
    
    nieSciezka=[]
    for j in range(iloscMiast):
        sciezkaNP=np.array(sciezka)
        if(np.sum((sciezkaNP==j).astype(int))==0):
           nieSciezka.append(j)
    nieSciezka=np.array(nieSciezka)
    #print("niesciezka",nieSciezka)
    #print("sciezka",sciezka)         #Utworzenie losowej sciezki
    kosztLaczny=0                           #Utworzenie zmiennej na łączny koszt
    
    #############################################
    #greedy, wymiana krawedzi
    #############################################
    indeks1=0
    indeks2=0
    fl1=False
    fl2=False
    while(indeks1!=1 or indeks2!=1):
        
        fl1=False#############
        indeks1=0##############
        while(fl1!=True):
            best1=(-1,-1,ObliczLacznyKoszt(odleglosciWzorzec,sciezka))   #(indeksNieSciezka,indeksSciezka,koszt)

            indeksySciezki=ciagLosowychCalkowitych(sciezka.shape[0],sciezka.shape[0])
            indeksyNieSciezki=ciagLosowychCalkowitych(nieSciezka.shape[0],nieSciezka.shape[0])
            for indeksNieSciezka in indeksyNieSciezki:
                for indeksSciezka in indeksySciezki:
                    Betterfound=False
                    sciezkacopy=copy.deepcopy(sciezka)
                    sciezkacopy[indeksSciezka]=nieSciezka[indeksNieSciezka]
                    if best1[2]>ObliczLacznyKoszt(odleglosciWzorzec,sciezkacopy):
                        best1=(indeksNieSciezka,indeksSciezka,ObliczLacznyKoszt(odleglosciWzorzec,sciezkacopy))
                        Betterfound=True
                        break
                if Betterfound==True:
                    break
            if best1[0]!=-1:
                pom=nieSciezka[best1[0]]
                nieSciezka[best1[0]]=sciezka[best1[1]]
                sciezka[best1[1]]=pom
            else: fl1=True
            indeks1+=1
            
        fl2=False############
        indeks2=0###########
        while(fl2!=True): #and indeks<1000000):
            best2=(-1,-1,ObliczLacznyKoszt(odleglosciWzorzec,sciezka))   #(indeksNieSciezka,indeksSciezka,koszt)
            #print(sciezka)
            indeksySciezki=ciagLosowychCalkowitych(sciezka.shape[0],sciezka.shape[0])
            indeksySciezki2=ciagLosowychCalkowitych(nieSciezka.shape[0],nieSciezka.shape[0])
            for indeksSciezka2 in indeksySciezki2:
                #print(i, indeksSciezka2)
                Betterfound=False
                for indeksSciezka in indeksySciezki:
                    poczatek=0
                    koniec=0
                    #if indeksSciezka2>indeksSciezka: 
                    #    poczatek=indeksSciezka
                    #    koniec=indeksSciezka2
                    #else:
                    #    poczatek=indeksSciezka2
                    #    koniec=indeksSciezka
                    poczatek=indeksSciezka
                    koniec=indeksSciezka2
                    sciezkacopy=copy.deepcopy(sciezka)
                    for index in range((koniec-poczatek)%sciezka.shape[0]+1):
                        sciezkacopy[(poczatek+index)%sciezka.shape[0]]=sciezka[(koniec-index)%sciezka.shape[0]]
                    if best2[2]>ObliczLacznyKoszt(odleglosciWzorzec,sciezkacopy) and poczatek!=koniec:
                        best2=(poczatek,koniec,ObliczLacznyKoszt(odleglosciWzorzec,sciezkacopy))
                        Betterfound=True
                        break
                if Betterfound==True:
                    break
            if best2[0]!=-1:
                poczatek=best2[0]
                koniec=best2[1]
                sciezkacopy=copy.deepcopy(sciezka)
                for index in range((koniec-poczatek)%sciezka.shape[0]+1):
                    sciezka[(poczatek+index)%sciezka.shape[0]]=sciezkacopy[(koniec-index)%sciezka.shape[0]]                
                
            else: fl2=True
            indeks2+=1
            
            #print(poczatek,koniec)
            
    kosztLaczny=ObliczLacznyKoszt(odleglosciWzorzec,sciezka)
    #print(sciezka)
    opis="Greedy wym. krawedzi, "+plik+", odleglosc="+str(kosztLaczny)
    duration=time.time()-startTime#########################################################################################################
    
    zbiorRozwiazan.append(Rozwiazanie(sciezkaDoPliku,sciezka,kosztLaczny,startMiasto,opis,duration))#########################################################################################################
rozwMin=2**32
rozwMax=0
rozwSr=0 
rozwCzasMin=2**32
rozwCzasMax=0
rozwCzasSr=0
ilRozw=0
rozwNajlepsze=0  
for rozw in zbiorRozwiazan:
    ilRozw+=1
    if rozw.Koszt()>rozwMax:
        rozwMax=rozw.Koszt()
    if rozw.Koszt()<rozwMin:
        rozwMin=rozw.Koszt()
        rozwNajlepsze=ilRozw-1
    rozwSr+=rozw.Koszt()
    if rozw.Czas()>rozwCzasMax:
        rozwCzasMax=rozw.Czas()
    if rozw.Czas()<rozwCzasMin:
        rozwCzasMin=rozw.Czas()
    rozwCzasSr+=rozw.Czas()
rozwSr=rozwSr/ilRozw
rozwCzasSr=rozwCzasSr/ilRozw
print("Greedy, wymiana krawedzi")
print("Odleglosci: Minimum= ",rozwMin," Maksimum= ",rozwMax," Srednio= ",rozwSr)
print("Czasy: Minimim= ",rozwCzasMin," Maksimum= ", rozwCzasMax, " Srednio= ",rozwCzasSr)
zbiorRozwiazan[rozwNajlepsze].Rysuj()###########################################