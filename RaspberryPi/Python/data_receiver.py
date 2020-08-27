import os
import glob
import numpy as np
from datetime import datetime
import data_projection_classification as dpc

# paths
raspberry_path = os.path.dirname(os.path.dirname(__file__))
kernel_path = raspberry_path + '/IPython/.Kernel'
input_path = raspberry_path + '/IPython/Input'

N = 250 # numero de leituras para cada serie temporal
time_id = np.arange(1,N+1) # vetor sequencial para o id de tempo da serie temporal

old_csv = 0 # variavel de controle para saber se existe leituras novas

try:
    while True:
        try:
            # procura o arquivo .csv mais recente
            all_files = glob.glob(kernel_path + '/*.csv')
            latest_csv = max(all_files, key=os.path.getctime)
            existe_csv = True
        except:
            existe_csv = False # caso não seja encontrado nenhum arquivo .csv na pasta, não entrara no if

        # verifica se esse arquivo .csv mais recente ja foi verificado antes
        if latest_csv != old_csv and existe_csv:
            old_csv = latest_csv # modifica a variavel de controle old_csv para verificar nas proximas leituras

            raw_data = np.genfromtxt(latest_csv, skip_header=1) # recebe em formato de np.array o .csv mais recente

            rows, columns = raw_data.shape 
            data = np.zeros((rows, 8)) # a partir do tamanho dos dados brutos cria um novo array para os dados processados

            # preenche as duas primeiras colunas desse novo array com o id da serie temporal e como o time_id
            # rows/N deve sempre um numero inteiro, ja que as series temporais salvas devem ter todas o mesmo tamanho N
            for i in range(int(rows/N)):
                data[i*N:(i+1)*N,0] = N*[i+1]
                data[i*N:(i+1)*N,1] = time_id

            data[:,2:] = raw_data[:,0:6] # os dados brutos dos 6 primeiros canais são passados para o array com os dados divididos

            # salva o array formatado na pasta input
            now = datetime.now()
            timestr = now.strftime("%Y-%m-%d__%H-%M-%S")  
            np.savetxt(input_path+'/new_data_{}.csv'.format(timestr), data, delimiter=',')

            ### -------- final da formatação -------- ###

            features = dpc.dynamic_tsfresh()

            projected_data = dpc.PCA_projection(features)

            dpc.Model_Predict(projected_data)



except KeyboardInterrupt: # finaliza o loop infinito com ctrl+C
    print("EOF")