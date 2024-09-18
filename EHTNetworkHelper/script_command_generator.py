from EHTNetworkHelper import EHTNetworkHelper

def teste_nStations(eht_helper, output_name='teste'):
    """criar um conjunto de comandos de simulações variando a distancia d"""
    with open(f'{output_name}.txt', 'w') as arquivo:
        # Escrevendo uma linha de texto no arquivo
        arquivo.write(f'')
    for i in range(5):
        new_nStations = eht_helper.nStations + 30 * i
        print(new_nStations)
        eht_helper.nStations = new_nStations

        saida = eht_helper.generate_run_command()
        # Abrindo (ou criando) o arquivo no modo de escrita ('w')
        with open(f'{output_name}.txt', 'a') as arquivo:
            # Escrevendo uma linha de texto no arquivo
            arquivo.write(f'{saida}\n')
    pass

helper = EHTNetworkHelper(
    ns3_path=r"/home/william/ns-3/ns-allinone-3.40/ns-3.40",
    script_name="william-eht",
    enable_op_params=True
)

helper.frequency = 5

helper.mcs=10
helper.cw=40
helper.nStations = 10

teste_nStations(helper, '5GHz')

helper.frequency2 = 6
helper.nStations = 10

teste_nStations(helper, '5GHz_6GHz')
