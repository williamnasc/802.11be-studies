import os

from EHTNetworkHelper import EHTNetworkHelper

def teste_nStations(eht_helper, output_name='teste'):
    """criar um conjunto de comandos de simulações variando a distancia d"""
    with open(f'{output_name}.txt', 'w') as arquivo:
        # Escrevendo uma linha de texto no arquivo
        arquivo.write(f'')
    inicial_nStations = eht_helper.nStations
    for i in range(4):
        new_nStations = eht_helper.nStations + 30 * i
        print(new_nStations)
        eht_helper.nStations = new_nStations

        saida = eht_helper.generate_run_command(
            output_file_name=str(output_name+'_'+str(new_nStations))
        )
        # Abrindo (ou criando) o arquivo no modo de escrita ('w')
        with open(f'{output_name}.txt', 'a') as arquivo:
            # Escrevendo uma linha de texto no arquivo
            arquivo.write(f'{saida}\n')
    pass
    eht_helper.nStations = inicial_nStations



helper = EHTNetworkHelper(
    script_name="wifi-eht-network",
)

helper.nStations = 1
helper.mcs=11
helper.simulationTime=1


params_matrix = [
    (2.4, 0, 0),
    (2.4, 5, 0),
    (2.4, 6, 0),
    (2.4, 5, 6),
]
sh_names = []
pasta = "teste_24"
os.mkdir(pasta)
for i, params in enumerate(params_matrix):
    freq, freq2, freq3 = params
    helper.frequency = freq
    helper.frequency2 = freq2
    helper.frequency3 = freq3
    print(f"creating for: {freq}_{freq2}_{freq3}")
    sh_name = helper.generate_sh_script(
        output_sim_path=r"/results_teste/Sim_"+str(i+10)+str(f"_{int(freq)}")+str(f"_{int(freq2)}")+str(f"_{int(freq3)}"),
        sh_name=f"ns3_sim_{str(i+10)}_{int(freq)}_{int(freq2)}_{int(freq3)}",
        folder=pasta)
    sh_names.append(sh_name)

helper.runner_sh_scripts(sh_names=sh_names, file_name=pasta)


params_matrix = [
    (5, 0, 0),
    (5, 2.4, 0),
    (5, 6, 0),
    (5, 2.4, 6),
]
sh_names = []
pasta = "teste_5"
os.mkdir(pasta)
for i, params in enumerate(params_matrix):
    freq, freq2, freq3 = params
    helper.frequency = freq
    helper.frequency2 = freq2
    helper.frequency3 = freq3
    print(f"creating for: {freq}_{freq2}_{freq3}")
    sh_name = helper.generate_sh_script(
        output_sim_path=r"/results_teste/Sim_"+str(i+10)+str(f"_{int(freq)}")+str(f"_{int(freq2)}")+str(f"_{int(freq3)}"),
        sh_name=f"ns3_sim_{str(i+20)}_{int(freq)}_{int(freq2)}_{int(freq3)}",
        folder=pasta)
    sh_names.append(sh_name)

helper.runner_sh_scripts(sh_names=sh_names, file_name=pasta)

params_matrix = [
    (6, 0, 0),
    (6, 2.4, 0),
    (6, 5, 0),
    (6, 2.4, 5),
]
sh_names = []
pasta = "teste_6"
os.mkdir(pasta)
for i, params in enumerate(params_matrix):
    freq, freq2, freq3 = params
    helper.frequency = freq
    helper.frequency2 = freq2
    helper.frequency3 = freq3
    print(f"creating for: {freq}_{freq2}_{freq3}")
    sh_name = helper.generate_sh_script(
        output_sim_path=r"/results_teste/Sim_"+str(i+10)+str(f"_{int(freq)}")+str(f"_{int(freq2)}")+str(f"_{int(freq3)}"),
        sh_name=f"ns3_sim_{str(i+30)}_{int(freq)}_{int(freq2)}_{int(freq3)}",
        folder=pasta)
    sh_names.append(sh_name)

helper.runner_sh_scripts(sh_names=sh_names, file_name=pasta)


