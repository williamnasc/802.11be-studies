import time
import subprocess 

class EHTNetworkHelper:
    """Classe que facilitar a execução do eht-network do ns3"""

    def __init__(self,
                 ns3_path=r"/home/william/ns-3/ns-allinone-3.41/ns-3.41",
                 ):
        self.ns3_path = ns3_path

        self.frequency = 5  # FREQ DO PRIMEIRO LINK (2.4; 5; 6) [padrão = 5]
        self.frequency2 = 0  # FREQ DO SEGUNDO LINK (0 INDICA Q ESTA DESLIGADO) [0]
        self.frequency3 = 0  # FREQ DO TERCEIRO LINK (0 INDICA Q ESTA DESLIGADO) [0]
        self.distance = 1  # DISTANCIA DO STA AO AP EM METROS [padrão = 1]
        self.simulationTime = 0.1  # TEMPO DE SIMULACAO EM SEGUNDOS [10]
        self.udp = 0  # UDP if set to 1, TCP otherwise [true]
        self.downlink = 1  # Generate downlink flows if set to 1, uplink flows otherwise [true]
        self.useRts = 0  # Enable/disable RTS/CTS [false]
        self.useExtendedBlockAck = 0  # Enable/disable use of extended BACK [false]
        self.nStations = 1  # Number of non-AP HE stations [1]
        self.dlAckType = 'NO-OFDMA'  # Ack sequence type for DL OFDMA (NO-OFDMA, ACK-SU-FORMAT, MU-BAR, AGGR-MU-BAR) [NO-OFDMA]
        self.enableUlOfdma = 0  # Enable UL OFDMA (useful if DL OFDMA is enabled and TCP is used) [false]
        self.enableBsrp = 0  # Enable BSRP (useful if DL and UL OFDMA are enabled and TCP is used) [false]
        # muSchedAccessReqInterval =  # Duration of the interval between two requests for channel access made by the MU scheduler [+0fs]
        self.mcs = 11  # if set, limit testing to a specific MCS (0-11) [-1]
        self.payloadSize = 700  # The application payload size in bytes [700]
        # tputInterval =              # duration of intervals for throughput measurement [+0fs]
        self.minExpectedThroughput = 0  # if set, simulation fails if the lowest throughput is below this value [0]
        self.maxExpectedThroughput = 0  # if set, simulation fails if the highest throughput is above this value [0]

    def build_simulation_args(self):
        # argumentos da simulacao
        simulationTime_text = f" --simulationTime={self.simulationTime}"
        frequency_text = f" --frequency={self.frequency}"
        useRts_text = f" --useRts=0"
        minExpectedThroughput_text = " --minExpectedThroughput=6"
        maxExpectedThroughput_text = " --maxExpectedThroughput=550"
        mcs_text = f" --mcs={self.mcs}"

        frequency2_text = f" --frequency2={self.frequency2}"
        frequency3_text = f" --frequency3={self.frequency3}"
        distance_text = f" --distance={self.distance}"
        udp_text = f" --udp={self.udp}"
        downlink_text = f" --downlink={self.downlink}"
        useExtendedBlockAck_text = f" --useExtendedBlockAck={self.useExtendedBlockAck}"
        nStations_text = f" --nStations={self.nStations}"
        dlAckType_text = f" --dlAckType={self.dlAckType}"
        enableUlOfdma_text = f" --enableUlOfdma={self.enableUlOfdma}"
        enableBsrp_text = f" --enableBsrp={self.enableBsrp}"
        # muSchedAccessReqInterval =  # Duration of the interval between two requests for channel access made by the MU scheduler [+0fs]
        payloadSize_text = f" --payloadSize={self.payloadSize}"
        # tputInterval =              # duration of intervals for throughput measurement [+0fs]

        # SETANDO OS PARAMETROS DO OCMANDO DA SIMULACAO
        
        list_of_params = [
            simulationTime_text,
            frequency_text,
            frequency2_text,
            frequency3_text,
            udp_text,
            useRts_text,
            mcs_text,
            distance_text,
            nStations_text,
            dlAckType_text,
            enableUlOfdma_text,
            useExtendedBlockAck_text,
        ]

        if self.frequency2 is not None:
            list_of_params.append(frequency2_text)
        if self.frequency3 is not None:
            list_of_params.append(frequency3_text)
        
        # MONTA O COMANDO DA SIMULACAO COM OS ARGUMENTOS
        simulation_args = f"'wifi-eht-network "
        for param in list_of_params:
            simulation_args += param
        simulation_args += "'"

        return simulation_args

    def run(self, output_file_name="teste"):
        exe_ns3 = "/home/william/ns-3/ns-allinone-3.40/ns-3.40/ns3"
        command = "run"
        simulation_args = self.build_simulation_args()

        print(exe_ns3, command, simulation_args)
        return 0
        # RUN MODE
        # result = subprocess.run([exe_ns3, command, simulation_args], capture_output=True)
        #
        # self.save_output(result, output_file_name)
        #
        # return result

    def test_run(self):
        print("comando:", runner.build_simulation_args())
        print("RODANDO...")
        resultado = runner.run()
        print("RESULTADO \n", resultado.stdout.decode("utf-8"))

    def save_output(self, resultado, output_file_name):
        # SALVA A SAIDA EM UM ARQUIVO
        
        # PEGAR O INSTANTE DE TEMPO PARA N TER NOME DE ARQUIVOS REPETIDOS
        time_millisec = int(round(time.time() * 1000))

        # Defina o caminho completo do arquivo
        caminho = f"resultados_william/{output_file_name}_{time_millisec}.txt"
        print(f"output_f: {caminho}")

        output = resultado.stdout.decode("utf-8")
        linhas = output.splitlines()[2:] # ELIMINA AS 2 PRIMEIRAS LINHAS DA SAIDA
        output_tratado = "\n".join(linhas)

        # Abra o arquivo para escrita
        with open(caminho, "w") as arquivo:
            # Escreva no arquivo
            arquivo.write(output_tratado)

        pass

if __name__=='__main__':
    print('olá mundo!')
    helper = EHTNetworkHelper()
    helper.run()