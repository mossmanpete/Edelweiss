import random
import socket

from test import *

from Adversaries.SynHerdingBenchmarkAttacker import *
from Experiment.Experiment import *
from Experiment.ExperimentSetting import *
from Test.Report import *
from Util.Util import *
ip_to_seed_dict = {
    247: 300,
    217: 500,
    182: 700,
    242: 900, 
    185: 11000,
    220: 1300,
    214: 1500,
    165: 1700,
    212: 1900,
    190: 2100,
    213:2300}

# do a single experiment times


def AtomicStat(f, setting, times):
    stat_dict = {'Consistency': 0, 'Validity': 0, 'Unanimity': 0}
    for i in range(times):
        setting.set_seed(i+ip_to_seed_dict[int((get_host_ip().split('.'))[3])])
        # if times == 1:
        #     run_and_print(setting)
        #     return
        res = run_and_get_result(setting)
        for k, v in stat_dict.items():
            if not res[k]:
                stat_dict[k] = v+1
    for k, v in stat_dict.items():
        stat_dict[k] = v/times
    print(stat_dict, file=f)
    if f:
        f.flush()

# set parameter and run


def SetStatParaAndRun(_file, setting, input, times, f, tf, protocol, adversary, _lambda=1, k=1, centralized=True):
    setting.set_input(input)
    setting.set_n(len(input))
    setting.set_f(f)
    setting.set_tf(tf)
    setting.set_protocol(protocol)
    setting.set_centralized(centralized)
    if centralized:
        setting.set_centralized_adversary(adversary)
    else:
        setting.set_adversary(adversary)
    setting.set_lambda(_lambda)
    setting.set_k(k)

    print("protocol="+setting.get_protocol().name, file=_file)
    if centralized:
        print("Centralized adversary!", file=_file)
        print("centralized_adversary=" +
              setting.get_centralized_adversary().name, file=_file)
    else:
        print("adversary="+setting.get_adversary().name, file=_file)
    print("times="+str(times), file=_file)
    print("k="+str(k), file=_file)
    print("lambda="+str(_lambda), file=_file)
    print("f="+str(f), file=_file)
    print("tf="+str(tf), file=_file)
    AtomicStat(_file, setting, times)  # atomtic one


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
# print(get_host_ip())

