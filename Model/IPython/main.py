import Data_Projection_Classification as dpc
import main_numpy as mn
#import multiprocessing
#from multiprocessing import Process
import tkinter as tk

def prediction(output_id):
    features = dpc.dynamic_tsfresh(output_id)

    projected_data = dpc.PCA_projection(features)

    label = dpc.Model_Predict(projected_data)
    
    return label

def acquisition():
    output_id = 1
    #PROCESSES = 2
    mn.acquire()
    #aq = Process(target=mn.acquire) # 
    #aq.start()
       
    label = prediction(output_id)
    #ret_value = multiprocessing.Value("d",0,lock=False)
    #pr = Process(target=prediction, args=(output_id, ret_value))
    #pr.start()
        
        
    #aq.join()
    #pr.join()
    
    #label = ret_value.value
    if label == 0:
        lbl.configure(text='Ferramenta Boa')
    else:
        lbl.configure(text='Ferramenta Ruim')



if __name__ == '__main__':
    
    window = tk.Tk()
    
    window.title("Model GUI")
    
    window.geometry('500x500')
    
    lbl = tk.Label(window, text="Condicao")
    
    lbl.grid(column=0, row=1)
    
    btn = tk.Button(window, text="Comecar Aquisicao", command=acquisition)
    
    btn.grid(column=0,row=0)
    
    window.mainloop()
        
        
        
        
