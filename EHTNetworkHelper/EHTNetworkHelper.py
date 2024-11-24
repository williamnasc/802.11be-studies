import time
import subprocess 

class EHTNetworkHelper:
    """Classe que facilitar a execução do eht-network do ns3"""

    def __init__(self,
                 ns3_path=r"/home/william/ns-3/ns-allinone-3.43/ns-3.43",
                 script_name="william-eht-network",
                 enable_op_params=False
                 ):
        self.ns3_path = ns3_path
        self.script_name = script_name

        self.frequency = None # 5  # FREQ DO PRIMEIRO LINK (2.4; 5; 6) [padrão = 5]
        self.frequency2 = None # 0  # FREQ DO SEGUNDO LINK (0 INDICA Q ESTA DESLIGADO) [0]
        self.frequency3 = None # 0  # FREQ DO TERCEIRO LINK (0 INDICA Q ESTA DESLIGADO) [0]
        self.distance = None # 1  # DISTANCIA DO STA AO AP EM METROS [padrão = 1]
        self.simulationTime = None # 0.1  # TEMPO DE SIMULACAO EM SEGUNDOS [10]
        self.udp = None # 0  # UDP if set to 1, TCP otherwise [true]
        self.downlink = None # 1  # Generate downlink flows if set to 1, uplink flows otherwise [true]
        self.useRts = None # 0  # Enable/disable RTS/CTS [false]
        self.useExtendedBlockAck = None # 0  # Enable/disable use of extended BACK [false]
        self.nStations = None # 1  # Number of non-AP HE stations [1]
        self.dlAckType = None # 'NO-OFDMA'  # Ack sequence type for DL OFDMA (NO-OFDMA, ACK-SU-FORMAT, MU-BAR, AGGR-MU-BAR) [NO-OFDMA]
        self.enableUlOfdma = None # 0  # Enable UL OFDMA (useful if DL OFDMA is enabled and TCP is used) [false]
        self.enableBsrp = None # 0  # Enable BSRP (useful if DL and UL OFDMA are enabled and TCP is used) [false]
        # muSchedAccessReqInterval =  # Duration of the interval between two requests for channel access made by the MU scheduler [+0fs]
        self.mcs = None # 11  # if set, limit testing to a specific MCS (0-11) [-1]
        self.payloadSize = None # 700  # The application payload size in bytes [700]
        # tputInterval =              # duration of intervals for throughput measurement [+0fs]
        self.minExpectedThroughput = None # 0  # if set, simulation fails if the lowest throughput is below this value [0]
        self.maxExpectedThroughput = None # 0  # if set, simulation fails if the highest throughput is above this value [0]

        self.emlsrLinks = None # "0,1" # The comma separated list of IDs of EMLSR links (for MLDs only)
        # TODO > CONFIGURAR ESSES PARAMS NO BUILD SIMULATOR ARGS
        self.emlsrPaddingDelay = None # The EMLSR padding delay in microseconds (0, 32, 64, 128 or 256)
        self.emlsrTransitionDelay = None # The EMLSR transition delay in microseconds (0, 16, 32, 64, 128 or 256)
        self.emlsrAuxSwitch = None # "Whether Aux PHY should switch channel to operate on the link on which. The Main PHY was operating before moving to the link of the Aux PHY. "
        self.emlsrAuxChWidth = None  # The maximum channel width (MHz) supported by Aux PHYs.
        self.emlsrAuxTxCapable = None # Whether Aux PHYs are capable of transmitting.
        self.channelSwitchDelay = None # The PHY channel switch delay in microseconds

        # CUSTOM PARAMS
        self.enable_op_params = enable_op_params
        self.cw = 80
        self.gi = 800
        self.emlsr = 0


    def build_simulation_args(self):
        list_of_params = []

        # argumentos da simulacao
        if not (self.simulationTime is None):
            simulationTime_text = f" --simulationTime={self.simulationTime}"
            list_of_params.append(simulationTime_text)
        if not (self.frequency is None):
            frequency_text = f" --frequency={self.frequency}"
            list_of_params.append(frequency_text)
        if not (self.useRts is None):
            useRts_text = f" --useRts=0"
            list_of_params.append(useRts_text)
        if not (self.minExpectedThroughput is None):
            # TODO > AJUSTAR ESSE PARAM
            minExpectedThroughput_text = " --minExpectedThroughput=6"
            list_of_params.append(minExpectedThroughput_text)
        if not (self.maxExpectedThroughput is None):
            # TODO > AJUSTAR ESSE PARAM
            maxExpectedThroughput_text = " --maxExpectedThroughput=550"
            list_of_params.append(maxExpectedThroughput_text)
        if not (self.mcs is None):
            mcs_text = f" --mcs={self.mcs}"
            list_of_params.append(mcs_text)
        if not (self.frequency2 is None):
            frequency2_text = f" --frequency2={self.frequency2}"
            list_of_params.append(frequency2_text)
        if not (self.frequency3 is None):
            frequency3_text = f" --frequency3={self.frequency3}"
            list_of_params.append(frequency3_text)
        if not (self.distance is None):
            distance_text = f" --distance={self.distance}"
            list_of_params.append(distance_text)
        if not (self.udp is None):
            udp_text = f" --udp={self.udp}"
            list_of_params.append(udp_text)
        if not (self.downlink is None):
            downlink_text = f" --downlink={self.downlink}"
            list_of_params.append(downlink_text)
        if not (self.useExtendedBlockAck is None):
            useExtendedBlockAck_text = f" --useExtendedBlockAck={self.useExtendedBlockAck}"
            list_of_params.append(useExtendedBlockAck_text)
        if not (self.nStations is None):
            nStations_text = f" --nStations={self.nStations}"
            list_of_params.append(nStations_text)
        if not (self.dlAckType is None):
            dlAckType_text = f" --dlAckType={self.dlAckType}"
            list_of_params.append(dlAckType_text)
        if not (self.enableUlOfdma is None):
            enableUlOfdma_text = f" --enableUlOfdma={self.enableUlOfdma}"
            list_of_params.append(enableUlOfdma_text)
        if not (self.enableBsrp is None):
            enableBsrp_text = f" --enableBsrp={self.enableBsrp}"
            list_of_params.append(enableBsrp_text)
        # TODO > AJUSTAR ESSE PARAM
        # muSchedAccessReqInterval =  # Duration of the interval between two requests for channel access made by the MU scheduler [+0fs]
        if not (self.payloadSize is None):
            payloadSize_text = f" --payloadSize={self.payloadSize}"
            list_of_params.append(payloadSize_text)
        # TODO > AJUSTAR ESSE PARAM
        # tputInterval =              # duration of intervals for throughput measurement [+0fs]

        if not (self.emlsrLinks is None):
            emlsrLinks_text = f" --emlsrLinks={self.emlsrLinks}"
            list_of_params.append(emlsrLinks_text)


        # SETANDO OS PARAMETROS DO OCMANDO DA SIMULACAO


        if self.enable_op_params:
            cw_text = f" --cw={self.cw}"
            gi_text = f" --gi={self.gi}"
            emlsr_text = f" --emlsr={self.emlsr}"

            list_of_params.append(cw_text)
            list_of_params.append(gi_text)
            list_of_params.append(emlsr_text)

        # MONTA O COMANDO DA SIMULACAO COM OS ARGUMENTOS
        simulation_args = f"'{self.script_name} "
        for param in list_of_params:
            simulation_args += param
        simulation_args += "'"

        return simulation_args

    def run(self, output_file_name="teste"):
        # exe_ns3 = "/home/william/ns-3/ns-allinone-3.40/ns-3.40/ns3"
        exe_ns3 = self.ns3_path+"/ns3"

        command = "run"
        simulation_args = self.build_simulation_args()

        # RUN MODE
        result = subprocess.run([exe_ns3, command, simulation_args], capture_output=True)

        self.save_output(result, output_file_name)

        return result

    def generate_run_command(self,output_file_name="teste"):
        exe_ns3 = self.ns3_path+"/ns3"
        command = "run"
        simulation_args = self.build_simulation_args()

        out = exe_ns3 +' '+ command +' '+ simulation_args +' > '+ output_file_name+'.txt'
        return out

    def test_run(self):
        print("comando:", self.build_simulation_args())
        print("RODANDO...")
        resultado = self.run()
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
    helper.frequency = 5
    helper.frequency2 = 2.4
    helper.frequency3 = 6
    helper.run()