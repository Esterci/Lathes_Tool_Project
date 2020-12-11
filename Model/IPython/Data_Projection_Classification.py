import numpy as np
import pandas as pd
import pickle
import tsfresh
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
from sklearn.preprocessing import StandardScaler
from tsfresh.feature_extraction import extract_features
from tsfresh.feature_extraction.settings import from_columns
import os
import glob


def dynamic_tsfresh (output_id):

    #Changing Work Folder
    
    add_path1 = "/Input/"
    add_path2 = "/.Kernel/"
    add_path3 = "/StreamingData/"
    base_path = os.getcwd()
    working_path = os.getcwd()
    Input_path = working_path + add_path1
    Kernel_path = working_path + add_path2
    StreamingData_path = working_path + add_path3
    
    # Change folder to Kernel
    
    os.chdir( Kernel_path )

    # Load the the filtered features from the seed data-set

    features_filtered = pd.read_csv('features_filtered_{}.csv'.format(output_id))

    # Extract the useful information of it

    columns = np.array(features_filtered.columns)
    kind_to_fc_parameters = from_columns(features_filtered.columns)

    sensors_names = [None] * int(features_filtered.shape[1]);


    for i in range (columns.shape[0]):
        name = columns[i]
        c = '__';
        words = name.split(c)

        sensors_names[i] = words[0]

        '''if i < 20:

            print(name)
            print(words)
            print(features_names[i])
            print(sensors_names[i])
            print('_______')'''

    columns = columns.tolist()
    unique_sensors_names = np.unique(np.array(sensors_names))

    # Change folder to Input
    
    os.chdir( Kernel_path )
    
    scaler = pickle.load(open('scaler.sav', 'rb'))
    
    os.chdir( Input_path )

    # ----------------------------------------------------------------- #
    # Load the incoming data

    latest_csv = max(all_files, key=os.path.getctime)
    data = np.genfromtxt(lastest_csv, delimiter=',')
    data = data[:,0:6]
    L, W = data.shape
    
    data = scaler.transform(data)
    
    ts_id = 1
    LEN = 150
    time_id = list(range(1,LEN))
    
    for j in range(int(L/LEN)):
        new_data = np.zeros((LEN-1,8))
            
        new_data[:,0] = (LEN-1)*[ts_id]
        new_data[:,1] = time_id
        new_data[:,2:8] = data[LEN*j:LEN*(j+1)-1,:]
        
        if i == 1 and j == 0:
            total_data = new_data
        else:
            total_data = np.concatenate((total_data,new_data))
        ts_id += 1
    
    data_frame = pd.DataFrame(total_data, columns= ['id','time'] + ['Sensor_' + str(x) for x in range(1,(total_data.shape[1]-2))])
    
    # ----------------------------------------------------------------- #
    
    
    # Feature extraction guided by the seed data-set

    extraction_df = pd.DataFrame(data_frame.loc[::,'id':unique_sensors_names[0]].values,columns= ['id','time','Sensor'])
    #print(extraction_df.head())
    arrayList = [] 

    for sensor in unique_sensors_names:
        
        #print(extraction_df.head())
        #print('_____')
        extraction_df.loc[::,'Sensor'] = data_frame.loc[::,sensor]
        
        #print(extraction_df.head())
        #print('_____')
        
        extraction_df = extraction_df.rename(columns={'Sensor': sensor})
        
        tsfresh_parameters = kind_to_fc_parameters[sensor]
        
        extracted_features = extract_features(extraction_df, column_id="id", column_sort="time", default_fc_parameters=tsfresh_parameters)

        arrayList.append(extracted_features)

        extraction_df = extraction_df.rename(columns={sensor : 'Sensor'})    

    original_space_features = pd.concat(arrayList,axis=1)

    # Sort the features in accordance with the seed data-set
    
    original_space_features = original_space_features[columns]
    impute(original_space_features)
    original_space_features.sort_index(inplace = True)

    # Change folder to origin
    
    os.chdir( base_path )
    
    return original_space_features

def PCA_projection (features):
    
    #Changing Work Folder
        
    add_path3 = "/.Kernel/"
  
    base_path = os.getcwd()
    working_path = os.getcwd()
    Kernel_path = working_path + add_path3
        
    # Now change to PCA Figures directory

    os.chdir( Kernel_path )

    # load the model from disk
    loaded_pca = pickle.load(open('pca.sav', 'rb'))

    scaler = StandardScaler().fit(features)
    features_padronizadas = scaler.transform(features)

    features_reduzidas = loaded_pca.transform(features_padronizadas)
    
    print('Filtered Features')
    print('-' * 20)
    print(np.size(features_padronizadas,0))
    print(np.size(features_padronizadas,1))
    print('-' * 20)
    print('Reduced Features')
    print('-' * 20)
    print(np.size(features_reduzidas,0))
    print(np.size(features_reduzidas,1))
    
    # Now chance to base directory
    
    os.chdir( base_path )
    
    return features_reduzidas

def Model_Predict (projected_data):
    
    add_path2 = "/.Kernel/"
    add_path3 = "/.Recovery/"
    base_path = os.path.dirname(os.path.abspath("Model_Unified_Code.ipynb"))
    Kernel_path = base_path + add_path2
    
    # Now change to Kernel directory
    
    os.chdir( Kernel_path )
    
    model = pickle.load(open('model.sav', 'rb'))
    
    for i in range (projected_data.shape[0]):
        
        y_predict = model.predict(projected_data[i,:].reshape(1, -1))
    
        if y_predict[-1] == 0:
            print('Ferramenta Boa')
        else:
            print('Ferramenta Ruim')
    
        #print ('Label de Teste: %d' % int (projected_data[i]))
        print ('Label dado pela NN: %d' % int (y_predict[0]))
        print('___________________')
        print('                   ')
        
    # Now change to the base directory
    
    os.chdir( base_path )
    
    return y_predict[-1]
    
    
def prediction():
    features = dynamic_tsfresh()

    projected_data = PCA_projection(features)

    Model_Predict(projected_data)
    
    