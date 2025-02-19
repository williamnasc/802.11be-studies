import os

from EHTNetworkHelper import EHTNetworkHelper


helper = EHTNetworkHelper(
    script_name="wifi-eht-network",
)

list_num_stas = [1, 5, 10]

helper.nStations = 1
# helper.mcs=11
# helper.simulationTime=1

params_dict = {
    "params_matrix": [],
    "sh_names": [],
    "pasta": "nome",
    "list_num_stas": list_num_stas
}
params_dict_list = []
# #################################################################
params_matrix = [
    (2.4, 0, 0),
    (2.4, 5, 0),
    (2.4, 6, 0),
    (2.4, 5, 6),
]
sh_names = []
pasta = "teste_24"
params_dict = {
    "params_matrix": params_matrix,
    "sh_names": sh_names,
    "pasta": pasta,
    "list_num_stas": list_num_stas
}
params_dict_list.append(params_dict)
# #################################################################

params_matrix = [
    (5, 0, 0),
    (5, 2.4, 0),
    (5, 6, 0),
    (5, 2.4, 6),
]
sh_names = []
pasta = "teste_5"
params_dict = {
    "params_matrix": params_matrix,
    "sh_names": sh_names,
    "pasta": pasta,
    "list_num_stas": list_num_stas
}
params_dict_list.append(params_dict)
# #################################################################

params_matrix = [
    (6, 0, 0),
    (6, 2.4, 0),
    (6, 5, 0),
    (6, 2.4, 5),
]
sh_names = []
pasta = "teste_6"
params_dict = {
    "params_matrix": params_matrix,
    "sh_names": sh_names,
    "pasta": pasta,
    "list_num_stas": list_num_stas
}
params_dict_list.append(params_dict)
# #################################################################
for i, params_dict_sim in enumerate(params_dict_list):
    modos = ['str', 'emlsr']

    params_matrix = params_dict_sim["params_matrix"]
    list_num_stas = params_dict_sim["list_num_stas"]
    pasta = params_dict_sim["pasta"]
    os.mkdir(pasta)

    for num_stas in list_num_stas:
        helper.nStations = num_stas
        for modo in modos:

            for i, params in enumerate(params_matrix):
                freq, freq2, freq3 = params
                helper.frequency = freq
                helper.frequency2 = freq2
                helper.frequency3 = freq3

                if modo == "emlsr":
                    emlsrLinks = None
                    if freq2 != 0 and freq3 == 0:
                        emlsrLinks = "0,1"
                    elif (freq2 != 0) and (freq3 != 0):
                        emlsrLinks = "0,1,2"
                    helper.emlsrLinks = emlsrLinks
                else:
                    helper.emlsrLinks = None

                print(f"creating for: {freq}_{freq2}_{freq3} | modo:{modo} | stas: {num_stas}")
                sh_name = helper.generate_sh_script(
                    output_sim_path=r"/results_teste/Sim_" + str(i + 1) + str(f"_{int(freq)}") + str(
                        f"_{int(freq2)}") + str(f"_{int(freq3)}_{modo}_{num_stas}"),
                    sh_name=f"ns3_sim_{str(i + 1)}_{int(freq)}_{int(freq2)}_{int(freq3)}_{modo}_{num_stas}",
                    folder=pasta)
                sh_names.append(sh_name)
                pass
            helper.runner_sh_scripts(sh_names=sh_names, file_name=pasta)
            pass
        pass



