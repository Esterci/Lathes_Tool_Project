print('\n.: Welcome to our Autonomous Model Users\' Interface (AMUI)! :.' )
recovery_decision = input('\nWould you like to recover the previous analyses\' variables?(y/n) ')

recovery_decision = recovery_decision.strip()

import Model_Functions as mf
import numpy as np
import pandas as pd

if recovery_decision == 'y': #Recovering Data from previous analyse

    #Recovering Data from previous analyse

    print('Recovery Control Output')
    print('----------------------------------')

    D_S_parameters =  mf.Recovery('D_S_parameters') 
    ExtractedNames =  mf.Recovery('ExtractedNames') 
    SelectedFeatures =  mf.Recovery('SelectedFeatures') 
    ReducedFeatures =  mf.Recovery('ReducedFeatures') 
    SODA_parameters, processing_parameters =  mf.Recovery ('SODA_parameters_processing_parameters') 
    ClassificationPar =  mf.Recovery('ClassificationPar')
    
    Output_ID = int(D_S_parameters['ID'])

    print('The current Data ID is ', Output_ID)
    
    print('__________________________________________')
    
    #Main Code

    mode_decision = input('\nChoose the analyse mode from the list below:\n\n1. Interactive Mode\n2. Direct Mode\n\nType a number and press ENTER: ').strip()

    if mode_decision == '1': #Interactive Mode script

        print('__________________________________________')
        print('\n.:Interactive Mode options:.\n\nSelect the steps you would like to run from the lis below:\n\n1. Data Slicer\n2. TSFRESH Extraction\n3. TSFRESH Selection\n4. PCA\n5. SODA & Grouping Algorithm\n6. Classification\n7. All above')

        input_string = input("\n Enter the numbers separated by space (e.g. 2 4 5) and press ENTER: ")

        print("\n")
        steps_list = input_string.split()

        if any(x == "1" for x in steps_list): # Data Slicer

            print('__________________________________________')
            print('\n.:Data Slicer options:.\n')

            n_id_per_slice = int(input('How many ID\'s to compose in the same slice?\n\nType a number and press ENTER: '))

            slice_mode = input('\nChoose the slicing mode from the list below:\n\n1. Boolean mode\n2. imminent Mode\n\nType a number and press ENTER: ')
            
            loop = 0

            while loop == 0:
            
                if slice_mode == '1':

                    D_S_parameters = mf.DataSlicer(Output_ID,n_id_per_slice,'Main Data')

                    loop += 1

                elif slice_mode == '2':

                    print('Option not ready yet, keep up with our releases.')
                    #D_S_parameters = mf.DataSlicer(Output_ID,n_id_per_slice,'Main Data')
                    exit()

                else :

                    print('Wrong entry, please choose again...')

                    slice_mode = input('\nChoose the slicing mode from the list below:\n\n1. Boolean mode\n2. imminent Mode\n\nType a number and press ENTER: ')

        elif any(x == "2" for x in steps_list): #TSFRESH_Extraction

            ExtractedNames = mf.TSFRESH_Extraction(D_S_parameters) #(Extração de atributos)

        elif any(x == "3" for x in steps_list): #TSFRESH_Selection
        
            SelectedFeatures = mf.TSFRESH_Selection(D_S_parameters,ExtractedNames) # (Parametros e resultados da divisão de dados)

        elif any(x == "4" for x in steps_list): #PCA

            print('___________________________________________')
            print('\n.:PCA preview:.')

            preview_decision = 'n' 

            while preview_decision == 'n':

                pc_num = int(input('\nHow many PCs you would like to use?\n\nType a number and press ENTER: '))

                ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Test') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                preview_decision = input('\nWould you like to proceed with this number of PCs ?(y/n) ').strip()

            print('__________________________________________')
            print('\n.:PCA options:.\n')

            pca_mode = int(input('\nChoose the PCA mode from the list below:\n\n1. Simple calcule\n2. Partial PC Analyses\n3. Complete PC Analyses\n\nType a number and press ENTER: '))
            
            loop = 0

            while loop == 0:

                if pca_mode == 1:

                    ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Calc') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                    loop = 1

                elif pca_mode == 2:

                    ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Analytics') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                    loop = 2

                elif pca_mode == 3:

                    ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Specific') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                    loop = 3

                else:

                    print('\nWrong entry, try again...')

                    pca_mode = int(input('\nChoose the PCA mode from the list below:\n\n1. Simple calcule\n2. Partial PC Analyses\n3. Complete PC Analyses\n\nType a number and press ENTER: '))
            
        elif any(x == "5" for x in steps_list): #SODA & Grouping

            print('__________________________________________')
            print('\n.:SODA options:.')

            min_g = float(input('\nChoose the SODA minimum grid size.\nType a number and press ENTER: '))

            max_g = float(input('\nChoose the SODA maximum grid size.\nType a number and press ENTER: '))
            
            pace = float(input('\nChoose the SODA pace for grid size.\nType a number and press ENTER: '))
        
        

            grouping_decision = 'y'

            while grouping_decision == 'y':

                print('__________________________________________')
                print('\n.:Grouping Algorithm options:.\n')

                min_g = float(input('\nChoose the Grouping Algorithm purity percentage of the data clouds. Type a number (between 0 and 100) and press ENTER: '))

                ClassificationPar = mf.GroupingAlgorithm(SODA_parameters,80, processing_parameters) # (Labels do SODA, Porcentagem de definição, numero de ID's boas, parametros de processamento)

                grouping_decision = input('Would you like to use another purity percentage?(y/n) ')

        elif any(x == "6" for x in steps_list): #Classification
            
            print('__________________________________________')
            print('\n.:Classification options:.\n')

            min_g = float(input('\nChoose the SODA minimum grid size.\nType a number and press ENTER: '))

            max_g = float(input('\nChoose the SODA maximum grid size.\nType a number and press ENTER: '))
            
            n_a = int(input('\nChoose the numbber of clssifications you want to performe \nType a number and press ENTER: '))

            loop = 0

            while loop == 0:

                plot_decision = input('\nDo you want to see the confuion matrix plot?(y/n) ')

                if plot_decision == 'y':

                    mf.Classification (ClassificationPar, 2,5, 1, plot_matrix=True) #(Parametros do data-set,  min_grid_size, max_grid_size, numero de vezes a simular, plotar matriz de confusão (True or False))

                    loop += 1
                
                elif plot_decision == 'n':

                    mf.Classification (ClassificationPar, 2,5, 1, plot_matrix=True) #(Parametros do data-set,  min_grid_size, max_grid_size, numero de vezes a simular, plotar matriz de confusão (True or False))

                    loop += 1

                else:

                    print('\nWrong entry, please try again...\n')

        elif any(x == '7' for x in steps_list): #All

            print('__________________________________________')
            print('\n.:Data Slicer options:.\n')

            n_id_per_slice = int(input('How many ID\'s to compose in the same slice?\n\nType a number and press ENTER: '))

            slice_mode = input('\nChoose the slicing mode from the list below:\n\n1. Boolean mode\n2. imminent Mode\n\nType a number and press ENTER: ')
            
            loop = 0

            while loop == 0:
            
                if slice_mode == '1':

                    D_S_parameters = mf.DataSlicer(Output_ID,n_id_per_slice,'Main Data')

                    loop += 1

                elif slice_mode == '2':

                    print('Option not ready yet, keep up with our releases.')
                    #D_S_parameters = mf.DataSlicer(Output_ID,n_id_per_slice,'Main Data')
                    exit()

                else :

                    print('Wrong entry, please choose again...')

                    slice_mode = input('\nChoose the slicing mode from the list below:\n\n1. Boolean mode\n2. imminent Mode\n\nType a number and press ENTER: ')

            ExtractedNames = mf.TSFRESH_Extraction(D_S_parameters) #(Extração de atributos)
        
            SelectedFeatures = mf.TSFRESH_Selection(D_S_parameters,ExtractedNames) # (Parametros e resultados da divisão de dados)

            print('___________________________________________')
            print('\n.:PCA preview:.')

            preview_decision = 'n' 

            while preview_decision == 'n':

                pc_num = int(input('\nHow many PCs you would like to use?\n\nType a number and press ENTER: '))

                ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Test') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                preview_decision = input('\nWould you like to proceed with this number of PCs ?(y/n) ').strip()

            print('__________________________________________')
            print('\n.:PCA options:.\n')

            pca_mode = int(input('\nChoose the PCA mode from the list below:\n\n1. Simple calcule\n2. Partial PC Analyses\n3. Complete PC Analyses\n\nType a number and press ENTER: '))
            
            loop = 0

            while loop == 0:

                if pca_mode == 1:

                    ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Calc') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                    loop = 1

                elif pca_mode == 2:

                    ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Analytics') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                    loop = 2

                elif pca_mode == 3:

                    ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Specific') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                    loop = 3

                else:

                    print('\nWrong entry, try again...')

                    pca_mode = int(input('\nChoose the PCA mode from the list below:\n\n1. Simple calcule\n2. Partial PC Analyses\n3. Complete PC Analyses\n\nType a number and press ENTER: '))
            
        
            print('__________________________________________')
            print('\n.:SODA options:.\n')

            min_g = float(input('\nChoose the SODA minimum grid size.\nType a number and press ENTER: '))

            max_g = float(input('\nChoose the SODA maximum grid size.\nType a number and press ENTER: '))
            
            pace = float(input('\nChoose the SODA pace for grid size.\nType a number and press ENTER: '))
        
            SODA_parameters, processing_parameters = mf.SODA(ReducedFeatures,min_g,(max_g + pace),pace) # (Features reduzidas, granularidade mínima, granularidade máxima, passo)

            grouping_decision = 'y'

            while grouping_decision == 'y':

                print('__________________________________________')
                print('\n.:Grouping Algorithm options:.\n')

                min_g = float(input('\nChoose the Grouping Algorithm purity percentage of the data clouds. Type a number (between 0 and 100) and press ENTER: '))

                ClassificationPar = mf.GroupingAlgorithm(SODA_parameters,80, processing_parameters) # (Labels do SODA, Porcentagem de definição, numero de ID's boas, parametros de processamento)

                grouping_decision = input('Would you like to use another purity percentage?(y/n) ')
            
            print('__________________________________________')
            print('\n.:Classification options:.\n')

            min_g = float(input('\nChoose the SODA minimum grid size.\nType a number and press ENTER: '))

            max_g = float(input('\nChoose the SODA maximum grid size.\nType a number and press ENTER: '))
            
            n_a = int(input('\nChoose the numbber of clssifications you want to performe \nType a number and press ENTER: '))

            loop = 0

            while loop == 0:

                plot_decision = input('\nDo you want to see the confuion matrix plot?(y/n) ')

                if plot_decision == 'y':

                    mf.Classification (ClassificationPar, 2,5, 1, plot_matrix=True) #(Parametros do data-set,  min_grid_size, max_grid_size, numero de vezes a simular, plotar matriz de confusão (True or False))

                    loop += 1
                
                elif plot_decision == 'n':

                    mf.Classification (ClassificationPar, 2,5, 1, plot_matrix=True) #(Parametros do data-set,  min_grid_size, max_grid_size, numero de vezes a simular, plotar matriz de confusão (True or False))

                    loop += 1

                else:

                    print('\nWrong entry, please try again...\n')

        else:

            print('None of the steps was chosen.')

    if mode_decision == '2': #Direct Mode script

        #Decision sequence

        #Data Slicer

        print('__________________________________________')
        print('\n.:Data Slicer options:.\n')

        n_id_per_slice = int(input('How many ID\'s to compose in the same slice?\n\nType a number and press ENTER: '))

        slice_mode = input('\nChoose the slicing mode from the list below:\n\n1. Boolean mode\n2. imminent Mode\n\nType a number and press ENTER: ')

        loop = 0 

        while loop == 0:
            
            if slice_mode == '1':

                loop += 1

            elif slice_mode == '2':

                print('Option not ready yet, keep up with our releases.')
    
                exit()

            else :

                print('Wrong entry, please choose again...')

                slice_mode = input('\nChoose the slicing mode from the list below:\n\n1. Boolean mode\n2. imminent Mode\n\nType a number and press ENTER: ')

        #PCA

        print('___________________________________________')
        print('\n.:PCA options:.\n')

        pc_num = int(input('\nHow many PCs you would like to use?\n\nType a number and press ENTER: '))

        pca_mode = int(input('\nChoose the PCA mode from the list below:\n\n1. Simple calcule\n2. Partial PC Analyses\n3. Complete PC Analyses\n\nType a number and press ENTER: '))

        loop = 0

        while loop == 0:

            if pca_mode == 1:

                loop = 1

            elif pca_mode == 2:

                loop = 2

            elif pca_mode == 3:

                loop = 3

            else:

                print('\nWrong entry, try again...')

                pca_mode = int(input('\nChoose the PCA mode from the list below:\n\n1. Simple calcule\n2. Partial PC Analyses\n3. Complete PC Analyses\n\nType a number and press ENTER: '))
            
        #SODA & Grouping
        
        print('__________________________________________')
        print('\n.:SODA options:.')

        min_g = float(input('\nChoose the SODA minimum grid size.\nType a number and press ENTER: '))

        max_g = float(input('\nChoose the SODA maximum grid size.\nType a number and press ENTER: '))
            
        pace = float(input('\nChoose the SODA pace for grid size.\nType a number and press ENTER: '))

        print('\n__________________________________________')
        print('\n.:Grouping Algorithm options:.\n')

        purity = float(input('\nChoose the Grouping Algorithm purity percentage of the data clouds. Type a number (between 0 and 100) and press ENTER: '))

        #Classification

        print('__________________________________________')
        print('\n.:Classification options:.\n')

        min_g = float(input('\nChoose the SODA minimum grid size.\nType a number and press ENTER: '))

        max_g = float(input('\nChoose the SODA maximum grid size.\nType a number and press ENTER: '))
            
        n_a = int(input('\nChoose the numbber of clssifications you want to performe \nType a number and press ENTER: '))

        loop = 0

        while loop == 0:

            plot_decision = input('\nDo you want to see the confuion matrix plot?(y/n) ')

            if plot_decision == 'y':

                loop += 1
                
            elif plot_decision == 'n':

                loop += 1

            else:

                print('\nWrong entry, please try again...\n')


        #Execution Step
        
        #Data Slicer 
            
        if slice_mode == '1':

            D_S_parameters = mf.DataSlicer(Output_ID,n_id_per_slice,'Main Data')

        elif slice_mode == '2':

            print('Option not ready yet, keep up with our releases.')
                #D_S_parameters = mf.DataSlicer(Output_ID,n_id_per_slice,'Main Data')

        #TSFRESH_Extraction

        ExtractedNames = mf.TSFRESH_Extraction(D_S_parameters) #(Extração de atributos)

        #TSFRESH_Selection

        SelectedFeatures = mf.TSFRESH_Selection(D_S_parameters,ExtractedNames) # (Parametros e resultados da divisão de dados)

        #PCA

        if pca_mode == 1:

            ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Calc') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))

        elif pca_mode == 2:

            ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Analytics') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))

        elif pca_mode == 3:

            ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Specific') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))

        #SODA & Grouping

        SODA_parameters, processing_parameters = mf.SODA(ReducedFeatures,min_g, max_g,pace) # (Features reduzidas, granularidade mínima, granularidade máxima, passo)

        ClassificationPar = mf.GroupingAlgorithm(SODA_parameters,purity, processing_parameters) # (Labels do SODA, Porcentagem de definição, numero de ID's boas, parametros de processamento)

        #Classification

        if plot_decision == 'y':

            mf.Classification (ClassificationPar, 2,5, 1, plot_matrix=True) #(Parametros do data-set,  min_grid_size, max_grid_size, numero de vezes a simular, plotar matriz de confusão (True or False))
                
        elif plot_decision == 'n':

            mf.Classification (ClassificationPar, 2,5, 1, plot_matrix=True) #(Parametros do data-set,  min_grid_size, max_grid_size, numero de vezes a simular, plotar matriz de confusão (True or False))

elif recovery_decision == 'n': #New analyse

    print('')
    print('__________________________________________')

    loop = 0

    Output_ID = input('\nWhich is the ID number you want to analyse?\n\nType the ID number and press ENTER: ')

    while loop ==0:
        
        try:
            
            np.genfromtxt('/home/thiago/Repositories/Lathes_Tool_Project/Model/Input/Output_' + Output_ID + '.csv', delimiter = ',')
            
            loop +=1
            print('__________________________________________')
        except:
            
            print('__________________________________________')
            print('\a\nCould not find this ID number, Try again or press Ctrl + C to quit.')
            Output_ID = input('\nType the ID number and press ENTER: ')

    #Main Code

    mode_decision = input('\nChoose the analyse mode from the list below:\n\n1. Interactive Mode\n2. Direct Mode\n\nType a number and press ENTER: ').strip()

    if mode_decision == '1': #Interactive Mode script

        print('__________________________________________')
        print('\n.:Data Slicer options:.\n')

        n_id_per_slice = int(input('How many ID\'s to compose in the same slice?\n\nType a number and press ENTER: '))

        slice_mode = input('\nChoose the slicing mode from the list below:\n\n1. Boolean mode\n2. imminent Mode\n\nType a number and press ENTER: ')
            
        loop = 0

        while loop == 0:
            
            if slice_mode == '1':

                D_S_parameters = mf.DataSlicer(Output_ID,n_id_per_slice,'Main Data')

                loop += 1

            elif slice_mode == '2':

                print('Option not ready yet, keep up with our releases.')
                #D_S_parameters = mf.DataSlicer(Output_ID,n_id_per_slice,'Main Data')
                exit()

            else :

                print('Wrong entry, please choose again...')

                slice_mode = input('\nChoose the slicing mode from the list below:\n\n1. Boolean mode\n2. imminent Mode\n\nType a number and press ENTER: ')

        ExtractedNames = mf.TSFRESH_Extraction(D_S_parameters) #(Extração de atributos)
        
        SelectedFeatures = mf.TSFRESH_Selection(D_S_parameters,ExtractedNames) # (Parametros e resultados da divisão de dados)

        print('___________________________________________')
        print('\n.:PCA preview:.')

        preview_decision = 'n' 

        while preview_decision == 'n':

            pc_num = int(input('\nHow many PCs you would like to use?\n\nType a number and press ENTER: '))

            ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Test') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
            preview_decision = input('\nWould you like to proceed with this number of PCs ?(y/n) ').strip()

        print('__________________________________________')
        print('\n.:PCA options:.\n')

        pca_mode = int(input('\nChoose the PCA mode from the list below:\n\n1. Simple calcule\n2. Partial PC Analyses\n3. Complete PC Analyses\n\nType a number and press ENTER: '))
            
        loop = 0

        while loop == 0:

            if pca_mode == 1:

                ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Calc') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                loop = 1

            elif pca_mode == 2:

                ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Analytics') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                loop = 2

            elif pca_mode == 3:

                ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Specific') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))
                loop = 3

            else:

                print('\nWrong entry, try again...')

                pca_mode = int(input('\nChoose the PCA mode from the list below:\n\n1. Simple calcule\n2. Partial PC Analyses\n3. Complete PC Analyses\n\nType a number and press ENTER: '))
            
        
        print('__________________________________________')
        print('\n.:SODA options:.\n')

        min_g = float(input('\nChoose the SODA minimum grid size.\nType a number and press ENTER: '))

        max_g = float(input('\nChoose the SODA maximum grid size.\nType a number and press ENTER: '))
            
        pace = float(input('\nChoose the SODA pace for grid size.\nType a number and press ENTER: '))
        
        SODA_parameters, processing_parameters = mf.SODA(ReducedFeatures,min_g,(max_g + pace),pace) # (Features reduzidas, granularidade mínima, granularidade máxima, passo)

        grouping_decision = 'y'

        while grouping_decision == 'y':

            print('__________________________________________')
            print('\n.:Grouping Algorithm options:.\n')

            min_g = float(input('\nChoose the Grouping Algorithm purity percentage of the data clouds. Type a number (between 0 and 100) and press ENTER: '))

            ClassificationPar = mf.GroupingAlgorithm(SODA_parameters,80, processing_parameters) # (Labels do SODA, Porcentagem de definição, numero de ID's boas, parametros de processamento)

            grouping_decision = input('Would you like to use another purity percentage?(y/n) ')
            
        print('__________________________________________')
        print('\n.:Classification options:.\n')

        min_g = float(input('\nChoose the SODA minimum grid size.\nType a number and press ENTER: '))

        max_g = float(input('\nChoose the SODA maximum grid size.\nType a number and press ENTER: '))
            
        n_a = int(input('\nChoose the numbber of clssifications you want to performe \nType a number and press ENTER: '))

        loop = 0

        while loop == 0:

            plot_decision = input('\nDo you want to see the confuion matrix plot?(y/n) ')

            if plot_decision == 'y':

                mf.Classification (ClassificationPar, 2,5, 1, plot_matrix=True) #(Parametros do data-set,  min_grid_size, max_grid_size, numero de vezes a simular, plotar matriz de confusão (True or False))

                loop += 1
                
            elif plot_decision == 'n':

                mf.Classification (ClassificationPar, 2,5, 1, plot_matrix=True) #(Parametros do data-set,  min_grid_size, max_grid_size, numero de vezes a simular, plotar matriz de confusão (True or False))

                loop += 1

            else:

                print('\nWrong entry, please try again...\n')

    if mode_decision == '2': #Direct Mode script

        #Decision sequence

        #Data Slicer

        print('__________________________________________')
        print('\n.:Data Slicer options:.\n')

        n_id_per_slice = int(input('How many ID\'s to compose in the same slice?\n\nType a number and press ENTER: '))

        slice_mode = input('\nChoose the slicing mode from the list below:\n\n1. Boolean mode\n2. imminent Mode\n\nType a number and press ENTER: ')

        loop = 0 

        while loop == 0:
            
            if slice_mode == '1':

                loop += 1

            elif slice_mode == '2':

                print('Option not ready yet, keep up with our releases.')
    
                exit()

            else :

                print('Wrong entry, please choose again...')

                slice_mode = input('\nChoose the slicing mode from the list below:\n\n1. Boolean mode\n2. imminent Mode\n\nType a number and press ENTER: ')

        #PCA

        print('___________________________________________')
        print('\n.:PCA options:.\n')

        pc_num = int(input('\nHow many PCs you would like to use?\n\nType a number and press ENTER: '))

        pca_mode = int(input('\nChoose the PCA mode from the list below:\n\n1. Simple calcule\n2. Partial PC Analyses\n3. Complete PC Analyses\n\nType a number and press ENTER: '))

        loop = 0

        while loop == 0:

            if pca_mode == 1:

                loop = 1

            elif pca_mode == 2:

                loop = 2

            elif pca_mode == 3:

                loop = 3

            else:

                print('\nWrong entry, try again...')

                pca_mode = int(input('\nChoose the PCA mode from the list below:\n\n1. Simple calcule\n2. Partial PC Analyses\n3. Complete PC Analyses\n\nType a number and press ENTER: '))
            
        #SODA & Grouping
        
        print('__________________________________________')
        print('\n.:SODA options:.')

        min_g = float(input('\nChoose the SODA minimum grid size.\nType a number and press ENTER: '))

        max_g = float(input('\nChoose the SODA maximum grid size.\nType a number and press ENTER: '))
            
        pace = float(input('\nChoose the SODA pace for grid size.\nType a number and press ENTER: '))

        print('\n__________________________________________')
        print('\n.:Grouping Algorithm options:.\n')

        purity = float(input('\nChoose the Grouping Algorithm purity percentage of the data clouds. Type a number (between 0 and 100) and press ENTER: '))

        #Classification

        print('__________________________________________')
        print('\n.:Classification options:.\n')

        min_g = float(input('\nChoose the SODA minimum grid size.\nType a number and press ENTER: '))

        max_g = float(input('\nChoose the SODA maximum grid size.\nType a number and press ENTER: '))
            
        n_a = int(input('\nChoose the numbber of clssifications you want to performe \nType a number and press ENTER: '))

        loop = 0

        while loop == 0:

            plot_decision = input('\nDo you want to see the confuion matrix plot?(y/n) ')

            if plot_decision == 'y':

                loop += 1
                
            elif plot_decision == 'n':

                loop += 1

            else:

                print('\nWrong entry, please try again...\n')


        #Execution Step
        
        #Data Slicer 
            
        if slice_mode == '1':

            D_S_parameters = mf.DataSlicer(Output_ID,n_id_per_slice,'Main Data')

        elif slice_mode == '2':

            print('Option not ready yet, keep up with our releases.')
                #D_S_parameters = mf.DataSlicer(Output_ID,n_id_per_slice,'Main Data')

        #TSFRESH_Extraction

        ExtractedNames = mf.TSFRESH_Extraction(D_S_parameters) #(Extração de atributos)

        #TSFRESH_Selection

        SelectedFeatures = mf.TSFRESH_Selection(D_S_parameters,ExtractedNames) # (Parametros e resultados da divisão de dados)

        #PCA

        if pca_mode == 1:

            ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Calc') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))

        elif pca_mode == 2:

            ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Analytics') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))

        elif pca_mode == 3:

            ReducedFeatures = mf.PCA_calc(SelectedFeatures,pc_num,'Specific') # (Feautures selecionadas, numero de PC's a manter, mode ('Test','Calc','Specific', 'Analytics'))

        #SODA & Grouping

        SODA_parameters, processing_parameters = mf.SODA(ReducedFeatures,min_g, max_g,pace) # (Features reduzidas, granularidade mínima, granularidade máxima, passo)

        ClassificationPar = mf.GroupingAlgorithm(SODA_parameters,purity, processing_parameters) # (Labels do SODA, Porcentagem de definição, numero de ID's boas, parametros de processamento)

        #Classification

        if plot_decision == 'y':

            mf.Classification (ClassificationPar, 2,5, 1, plot_matrix=True) #(Parametros do data-set,  min_grid_size, max_grid_size, numero de vezes a simular, plotar matriz de confusão (True or False))
                
        elif plot_decision == 'n':

            mf.Classification (ClassificationPar, 2,5, 1, plot_matrix=True) #(Parametros do data-set,  min_grid_size, max_grid_size, numero de vezes a simular, plotar matriz de confusão (True or False))

else: 

    print('Unavalable command, try again ...')
    exit()

"""
ModelPar = mf.Model_Train(ClassificationPar,'euclidean',"Neural Net",2.75) #(Parametros da data-set, distância, Modelo, granularidade)

mf.Model_Predict(ModelPar)
"""
