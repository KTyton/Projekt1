#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:31:47 2019

@author: prawienocski
"""
#import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QColorDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt #odpowiedzialny za rysowanie wykresu


class AppWindow(QWidget): #klasa reprezentujaca aplikacje
    def __init__(self):
        super().__init__()
        self.title = 'Przecięcia prostych'#tytuł
        self.initInterface() #klasa odpowiedzialna za tworzenie interfejsu
        self.initWidgets()
    
    def initInterface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(500,500,600,600) #geometria okna
        self.show() #wyswietlenie okna
        
    def initWidgets(self):
        btnCol = QPushButton('Wybierz kolor',self)#przycisk
        btn=QPushButton('Rysuj',self)
        btnsave=QPushButton('Zapisz wynik',self)
        xaLabel = QLabel('Xa',self)#sluzy nad do podpisywania 
        yaLabel = QLabel('Ya',self)
        xbLabel = QLabel('Xb',self)
        ybLabel = QLabel('Yb',self)
        xcLabel = QLabel('Xc',self)
        ycLabel = QLabel('Yc',self)
        xdLabel = QLabel('Xd',self)
        ydLabel = QLabel('Yd',self)
        xpLabel = QLabel('Xp',self)
        ypLabel = QLabel('Yp',self)
        NAPISLabel = QLabel('Gdzie się znajduję punkt ?',self)
        self.xpEdit = QLineEdit()#pole w ktorym wpisujemy tekst badz liczbe
        self.ypEdit = QLineEdit()
        self.xaEdit = QLineEdit()
        self.yaEdit = QLineEdit()
        self.xbEdit = QLineEdit()
        self.ybEdit = QLineEdit()
        self.xcEdit = QLineEdit()
        self.ycEdit = QLineEdit()
        self.xdEdit = QLineEdit()
        self.ydEdit = QLineEdit()
        self.NAPISEdit = QLineEdit()
        
        resultLabel = QLabel('',self)
         #wykres
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        grid = QGridLayout() #tworzenie siatki
        grid.addWidget(xaLabel,2,0)#2wiersz 0 kolumna
        grid.addWidget(self.xaEdit,2,1)
        grid.addWidget(yaLabel,3,0)
        grid.addWidget(self.yaEdit,3,1)
        grid.addWidget(xbLabel,4,0)
        grid.addWidget(self.xbEdit,4,1)
        grid.addWidget(ybLabel,5,0)
        grid.addWidget(self.ybEdit,5,1)
        grid.addWidget(xcLabel,6,0)
        grid.addWidget(self.xcEdit,6,1)
        grid.addWidget(ycLabel,7,0)
        grid.addWidget(self.ycEdit,7,1)
        grid.addWidget(xdLabel,8,0)
        grid.addWidget(self.xdEdit,8,1)
        
        grid.addWidget(xpLabel,10,0)
        grid.addWidget(self.xpEdit,10,1,1,2)
        grid.addWidget(ypLabel,11,0)
        grid.addWidget(self.ypEdit,11,1,1,2)
        grid.addWidget(NAPISLabel,12,0)
        grid.addWidget(self.NAPISEdit,13,0,1,4)
        
        grid.addWidget(ydLabel,9,0)
        grid.addWidget(self.ydEdit,9,1)
        grid.addWidget(btn,14,0,1,2)#czternasty wiersz, zerowa kolumna, rozciaga sie na jeden wiersz i dwie kolumny
        grid.addWidget(btnCol,15,0,1,2)
        grid.addWidget(btnsave,16,0,1,2)
        grid.addWidget(resultLabel,17,0)
        grid.addWidget(self.canvas,1,7,-1,-1)
        
        
        self.setLayout(grid)
        
        btn.clicked.connect(self.oblicz)#przycisk ktory za pomoca klikniecia wywoluje sygnal ktory w dalszej czesci cos robi 
        btnCol.clicked.connect(self.zmienKolor)
        btnsave.clicked.connect(self.zapisz)
        
    def zmienKolor(self):#definicja ktora otwiera nam palete z kolorami 
        color = QColorDialog.getColor()
        if color.isValid():
            print(color.name())
        self.robCos(col=color.name())
        
    def oblicz(self):#
        self.robCos()
    
    
    def robCos(self, col='red'):
        # plt.cla #czyszczenie wykresu
        xa = self.sprawdzenieWartosci(self.xaEdit)#sprawdzanie czy dane zostały zapisane poprawnie jak opisuje nam definicja sprawdzenieWartosci
        ya = self.sprawdzenieWartosci(self.yaEdit)
        xb = self.sprawdzenieWartosci(self.xbEdit)
        yb = self.sprawdzenieWartosci(self.ybEdit)
        xc = self.sprawdzenieWartosci(self.xcEdit)
        yc = self.sprawdzenieWartosci(self.ycEdit)
        xd = self.sprawdzenieWartosci(self.xdEdit)
        yd = self.sprawdzenieWartosci(self.ydEdit)
        if (xa is not None) and (ya is not None) and (xb is not None) and (yb is not None) and (xc is not None) and (yc is not None) and (xd is not None) and (yd is not None):
            if (((xb-xa)*(yd-yc))-((yb-ya)*(xd-xc)))==0:#przypadek równoległosci
                self.NAPISEdit.setText('proste są równoległe')
            else:#przypadki inne niż kiedy proste są względem siebie równoległe
                T1=(((xc-xa)*(yd-yc))-((yc-ya)*(xd-xc)))/(((xb-xa)*(yd-yc))-((yb-ya)*(xd-xc)))
                T2=(((xc-xa)*(yb-ya))-((yc-ya)*(xb-xa)))/(((xb-xa)*(yd-yc))-((yb-ya)*(xd-xc)))    
                self.xP=round(xa+T1*(xb-xa),3)
                self.yP=round(ya+T1*(yb-ya),3)
                if T1>0 and T1<1 and T2>0 and T2<1:#warunki
                    self.NAPISEdit.setText("punkt leży na przecięciu odcinków AB i CD")
                elif T1>0 and T1<1 and T2<0:
                    self.NAPISEdit.setText("przecięcie odcinka AB oraz przedłuzenie CD")
                elif T1>0 and T1<1 and T2>1:
                    self.NAPISEdit.setText("przecięcie odcinka AB oraz przedłuzenie CD")
                elif T2>0 and T2<1 and T1>1:
                    self.NAPISEdit.setText("przecięcie odcinka CD oraz przedłuzenie AB")
                elif T2>0 and T2<1 and T1<0:
                    self.NAPISEdit.setText("przecięcie odcinka CD oraz przedłuzenie AB")
                elif T2<0 or T2>1 and T1>1 or T1<0:
                    self.NAPISEdit.setText("na przedłużeniach odcinków AB i CD")
                
            self.xpEdit.setText(str(self.xP))
            self.ypEdit.setText(str(self.yP))
            x_1=['A', 'B', 'C', 'D', 'P']
            X_2=[xa, xb, xc, xd, self.xP]
            Y_2=[ya, yb, yc, yd, self.yP]
                      
            self.figure.clear()
            ax=self.figure.add_subplot(111)  
            ax.scatter(X_2,Y_2)
            ax.plot([xa,xb],[ya,yb] ,color=col,marker='o')#rysuje nam linie w dowolnym wybranym przez nas kolorze dzieki definicji zmienKolor
            ax.plot([xc,xd],[yc,yd] ,color=col,marker='o')
            ax.plot([xa,self.xP],[ya,self.yP] ,linestyle='--', color='red')#rysuje nam linie przerywaną o kolorze czerwonym
            ax.plot([xd,self.xP],[yd,self.yP] ,linestyle='--', color='blue')
            for (x,y,l) in zip(X_2,Y_2,enumerate(x_1)):#etykietowanie punktów
                ax.annotate("{}({};{})".format(l[1],x,y), xy=(x,y))
            self.canvas.draw()
            
    def zapisz(self):
        plik1=open('wspolrzedne.txt','w+')#stworzenie pliku tekstowego, ktory aktualizuje dane
        plik1.write(80*'-')
        plik1.write('\n|{:^10}|\n'.format('współrzędne'))#okrelenie formatu zapisu danych
        plik1.write('\n|{:^10}|{:^10}|\n'.format('xP', 'yP'))
        plik1.write('\n|{:^10}|{:^10}|\n'.format(self.xP,self.yP))
        plik1.close()
    
    def sprawdzenieWartosci(self,element): 
        if element.text().lstrip('-').replace('.','',1).isdigit():#sprawdzenie czy dane zostały zapisane w prawidłowy sposób, jesli nie obraz prostych nie zostane narysowany
            return float(element.text())
        else:
            element.setFocus() #zeby element byl widoczny
            return None 
        
if __name__ == '__main__':
    import sys
    
    app =  QApplication(sys.argv)
    okno = AppWindow()
    sys.exit(app.exec_())