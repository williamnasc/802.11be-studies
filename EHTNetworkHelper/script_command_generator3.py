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

helper.frequency = 5
helper.nStations = 10
helper.mcs=11
helper.simulationTime=10

teste_nStations(helper, 'be_5GHz')
