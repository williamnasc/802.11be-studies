import fileinput
import sys
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def list_file_n_foldes(dir_dist_path):
    """Lista quais sao as pastas e arquivos de um dado caminho"""
    # LISTA TUDO DENTRO DA PASTA
    arquivos = os.listdir(str(dir_dist_path))
    folders = []
    files = []
    for arquivo in arquivos:
        if os.path.isdir(dir_dist_path + r'/' + arquivo):
            folders.append(dir_dist_path + r'/' + arquivo)
        else:
            files.append(dir_dist_path + r'/' + arquivo)
    return files, folders


# WINDOWS
# folder_path = r'\\wsl.localhost\Ubuntu-20.04\home\william\ns-3\ns-allinone-3.40\ns-3.40\resultados_william'

# UBUNTU
# folder_path = r'/home/william/ns-3/ns-allinone-3.40/ns-3.40/resultados_william/2_link_distance_6_24hz'
# folder_path = r'/home/william/ns-3/ns-allinone-3.40/ns-3.40/resultados_william'
# folder_path = r'/home/william/ns-3/ns-allinone-3.40/ns-3.40/testes_emlsr'
# folder_path = r'/home/william/ns-3/ns-allinone-3.43/ns-3.43/testes_emlsr'
# folder_path = r'/home/william/downloads/results_teste3'
folder_path = r'/home/william/downloads/flow_testes'

# home\william\downloads\results_teste

banda_filter = 40
gi_filter = 800

files, folders = list_file_n_foldes(folder_path)

# print(files)
# print(folders)

columns = ['MCS', 'Channel_width', 'GI', 'Throughput', 'Frequency', 'Frequency2', 'Frequency3', 'numSTAs', 'STD']
all_data = pd.DataFrame(columns=columns)
# print(all_data)

for folder in folders:
    sim_files, sub_folders = list_file_n_foldes(folder)
    # for file_t in sim_files:
    #     print(f"sim_file: {file_t}")
    for i, file_t in enumerate(sim_files):
        print(f"arquivo: {i}")
        # PEGA DADOS DO TITULO DO ARQUIVO
        path_names = file_t.split('/')
        file_name = path_names[-1]
        simulation_title_parts = file_name.split('_')

        # standard = simulation_title_parts[0]
        # numSTAs = int(simulation_title_parts[-1].split('.')[0])
        # frequency = int(simulation_title_parts[1].replace('GHz', ''))
        # frequency2 = 0
        # frequency3 = 0
        # if 'GHz' in simulation_title_parts[2]:
        #     frequency2 = int(simulation_title_parts[2].replace('GHz', ''))
        # if len(simulation_title_parts) > 3 and 'GHz' in simulation_title_parts[3]:
        #     frequency3 = int(simulation_title_parts[3].replace('GHz',

        # print('dados:', standard, numSTAs, frequency, frequency2, frequency3)

        standard = 'be'
        numSTAs = int(simulation_title_parts[-1].split('.')[0])
        frequency = int(simulation_title_parts[2].replace('GHz', ''))
        frequency2 = int(simulation_title_parts[3].replace('GHz', ''))
        frequency3 = int(simulation_title_parts[4].replace('GHz', ''))
        mlo_mode = simulation_title_parts[5]

        if (frequency == 2): frequency = 2.4
        if (frequency2 == 2): frequency2 = 2.4
        if (frequency3 == 2): frequency3 = 2.4

        print(f'NOME : {simulation_title_parts}')
        print('dados:', standard, mlo_mode, numSTAs, frequency, frequency2, frequency3)
        # continue

        file_path = str(file_t)[:(len(file_t) - 4)]
        print(f"file_path: {file_path}")

        mean_PLR = None
        mean_Delay = None
        mean_Jitter = None

        simulation_files, simulation_sub_folders = list_file_n_foldes(file_path)
        # print(f"simulation_files: {simulation_files}")
        for sim_flow_file in simulation_files:
            if "Zone.Identifier" in sim_flow_file:
                continue
            if "DL" not in sim_flow_file:
                continue
            # print(sim_flow_file)
            # Carregar um arquivo CSV com separador ',' (padrão)
            df = pd.read_csv(sim_flow_file)
            # Mostrar as primeiras linhas
            # print(df.head())
            # print(df.columns)
            mean_PLR = df[" Packet_Loss_Ratio"].mean()
            mean_Delay = df[' Mean_Delay_Rx_Packets'].mean()
            mean_Jitter = df[' Mean_Jitter'].mean()

            print(f" mean_PLR: {mean_PLR}\n mean_Delay: {mean_Delay}\n mean_Jitter: {mean_Jitter}")

        file_path = file_t
        print(f"file_path: {file_path}")

        # Ler o arquivo de texto
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # print(f"lines: {len(lines)}")

        # Processar as linhas para extrair as informações
        data = []
        for line in lines[1:]:  # Pular o cabeçalho

            if 'Command' in line or 'MCS' in line or 'ninja' in line or 'Process' in line:
                continue

            # print(line)
            # RETIRA AS UNIDADES DOS DADOS
            line = line.replace('Mbit/s', '')
            line = line.replace('MHz', '')
            line = line.replace('ns', '')
            # print(line)

            # Dividir a linha por tabulações ou múltiplos espaços
            parts = line.split()
            print('parts:', parts)

            if not (parts[0]).isdigit():
                continue

            # # Adicionar os dados à lista
            mcs_value = int(parts[0])
            channel_width = int(parts[1])
            gi = int(parts[2])
            throughput = float(parts[3])

            # ADICIONA OS DADOS
            data.append(
                [mcs_value, channel_width, gi, throughput, frequency, frequency2, frequency3, numSTAs,
                 mlo_mode, mean_PLR, mean_Delay, mean_Jitter])

        # Criar um DataFrame a partir dos dados
        columns = ['MCS', 'Channel_width', 'GI', 'Throughput', 'Frequency', 'Frequency2', 'Frequency3', 'numSTAs',
                   'STD', 'PLR', 'Delay', 'Jitter']
        df = pd.DataFrame(data, columns=columns)

        # print(df)
        all_data = pd.concat([all_data, df], ignore_index=True)

        # FILTRO
        # subset_complex = df[((df['Channel_width'] == banda_filter) & (df['GI'] == gi_filter))]

        # TODO > DESCOBRIR COMO PEGA 1 VALOR ESPECIFICO DO DATA FRAME
        # TODO > POR ENQUANTO TO PASSANDO O MAIOR VALOR DO DF
        tput = all_data['Throughput']
        # print(tput)

        # linha_data = {'Distance': dist, 'Throughput': tput.max()}

print("all_data")
print(all_data)
