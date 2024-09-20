from EHTNetworkHelper import EHTNetworkHelper

def teste_nStations(eht_helper, output_name='teste'):
    """criar um conjunto de comandos de simulações variando a distancia d"""
    with open(f'{output_name}.txt', 'w') as arquivo:
        # Escrevendo uma linha de texto no arquivo
        arquivo.write(f'')
    inicial_nStations = eht_helper.nStations
    for i in range(5):
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


helper_ax = EHTNetworkHelper(
    ns3_path=r".",
    script_name="william-he",
    enable_op_params=True
)

helper_ax.frequency = 5
helper_ax.mcs=10
helper_ax.cw=40
helper_ax.nStations = 10

teste_nStations(helper_ax, 'ax_5GHz')

helper_ax.frequency = 6
helper_ax.mcs=10
helper_ax.cw=40
helper_ax.nStations = 10

teste_nStations(helper_ax, 'ax_6GHz')

helper_ax.frequency = 2.4
helper_ax.mcs=10
helper_ax.cw=40
helper_ax.nStations = 10

teste_nStations(helper_ax, 'ax_24GHz')

print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

helper = EHTNetworkHelper(
    ns3_path=r".",
    script_name="william-eht",
    enable_op_params=True
)

helper.frequency = 5
helper.mcs=10
helper.cw=40
helper.nStations = 10

teste_nStations(helper, 'be_5GHz')

helper.frequency = 6
helper.mcs=10
helper.cw=40
helper.nStations = 10

teste_nStations(helper, 'be_6GHz')

helper.frequency = 2.4
helper.mcs=10
helper.cw=40
helper.nStations = 10

teste_nStations(helper, 'be_24GHz')


helper.frequency = 5
helper.frequency2 = 6
helper.nStations = 10

teste_nStations(helper, 'be_5GHz_6GHz')

helper.frequency = 5
helper.frequency2 = 6
helper.frequency3 = 2.4
helper.nStations = 10

teste_nStations(helper, 'be_5GHz_6GHz_24GHz')
