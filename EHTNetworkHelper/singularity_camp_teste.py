import os

from EHTNetworkHelper import EHTNetworkHelper


cluster_path = "/home/wmcdnascimento/ns-allinone-3.43/ns-3.43/"
helper = EHTNetworkHelper(
    ns3_path=cluster_path,
    script_name="william-eht-network",
    enable_op_params=True,
)

list_num_stas = [1, 5, 10, 20, 30, 40]
list_mcs = [0, 6, 13]
list_gi = [800]
list_cw = [40]

helper.nStations = 1
# helper.mcs=11
# helper.simulationTime=1

params_dict = {
    "params_matrix": [],
    "sh_names": [],
    "pasta": "nome",
    "list_num_stas": list_num_stas,
    "list_mcs": list_mcs,
    "list_cw": list_cw,
    "list_gi": list_gi,
}
params_dict_list = []

params_matrix = [
    (2.4, 0, 0),
    (2.4, 6, 0),
    (6, 5, 0),
    (2.4, 6, 5),
]
sh_names = []
pasta = "teste_singularity"
params_dict = {
    "params_matrix": params_matrix,
    "sh_names": sh_names,
    "pasta": pasta,
    "list_num_stas": list_num_stas,
    "list_mcs": list_mcs,
    "list_cw": list_cw,
    "list_gi": list_gi,
}
params_dict_list.append(params_dict)

count = 0

# #################################################################
for i, params_dict_sim in enumerate(params_dict_list):
    modos = ['str', 'emlsr']

    params_matrix = params_dict_sim["params_matrix"]
    list_num_stas = params_dict_sim["list_num_stas"]
    list_mcs = params_dict_sim["list_mcs"]
    list_cw = params_dict_sim["list_cw"]
    list_gi = params_dict_sim["list_gi"]
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


                for mcs in list_mcs:
                    for cw in list_cw:
                        for gi in list_gi:

                            helper.mcs = mcs
                            helper.cw = cw
                            helper.gi = gi


                            print(f"creating sim {count} for: {freq}_{freq2}_{freq3} | modo:{modo} | stas: {num_stas} |"
                                  f"mcs: {mcs} | cw: {cw} | gi: {gi}")
                            sh_name = helper.generate_sh_script_npad(
                                output_sim_path=r"/singularity_job/Sim_"+ str(count) + str(i + 1) + str(f"_{int(freq)}") + str(
                                    f"_{int(freq2)}") + str(f"_{int(freq3)}_{modo}_{num_stas}"),
                                sh_name=f"sim_{str(count)}_{str(i + 1)}_{int(freq)}_{int(freq2)}_{int(freq3)}_{modo}_{num_stas}",
                                folder=pasta)
                            sh_names.append(sh_name)
                            count += 1
                            pass
                pass
            helper.runner_sh_scripts(sh_names=sh_names, file_name=pasta)
            pass
        pass
