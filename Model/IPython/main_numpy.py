import spidev
import time
import ads_numpy
import os
import csv
import numpy as np
from numpy import asarray
from numpy import savetxt
import RPi.GPIO as gpio

def acquire():
    
    #Changing Work Folder
    
    add_path3 = "/StreamingData/"
    working_path = os.getcwd()
    StreamingData_path = working_path + add_path3
    
    # Change folder to Kernel
    
    os.chdir( StreamingData_path )
    
    ad = ads_numpy.AQ()

    PIN=23        
    name = ad.archive("Aquisicao.csv");
    canal=np.zeros((1,2400), dtype=np.uint8)
    a=0
    while(a<1):
        if gpio.event_detected(PIN):
            valor = ad.get_register()
            #valor = ad.shift_reg()
            canal = np.array(valor, dtype=np.uint8)
            a=a+1

    i=0
    while(i<166):
        if gpio.event_detected(PIN):
            valor = ad.get_register()
            #valor = ad.shift_reg()
            canais = np.array(valor, dtype=np.uint8)
            canal = np.vstack((canal,canais))
            i=i+1
            
    else:
        print (canal)
        canal = np.reshape (canal, (-1, 16))
        savetxt(name, canal, fmt='%u', delimiter=',')
        dim=np.array([])
        dim= ad.dim_matrix(canal)
        n=dim[0]
        valor=np.empty([n,8], dtype = float)
        a=0
        for a in range (n):
            b=0
            for b in range (0,15,2):
                hi=canal[a,b]
                lo=canal[a,(b+1)]
                c =(b/2)
                c=round(c)
                v=ad.int_to_bol(hi,lo)
                valor[a,c]=v
            a=a+1
        name = ad.archive("Aquisicao.csv");
        savetxt(name, valor, fmt='%f', delimiter=',')
        anal=np.zeros((1,2400), dtype=np.uint8)
        gpio.cleanup()

   

    