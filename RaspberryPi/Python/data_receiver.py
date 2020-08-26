import glob
import os

os.chdir('/home/thiago/Repositories/Lathes_Tool_Project/RaspberryPi/IPython/Input/')

i = 0;

while i == 0:
    all_files = glob.glob('/home/thiago/Repositories/Lathes_Tool_Project/RaspberryPi/IPython/.Kernel/*.csv') #give path to your desired file path
    latest_csv = max(all_files, key=os.path.getctime)
    print (latest_csv)

os.chdir('/home/thiago/Repositories/Lathes_Tool_Project/RaspberryPi/IPython/')