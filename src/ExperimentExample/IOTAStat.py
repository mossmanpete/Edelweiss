from Test.TestConfig import *
from Protocols.HerdingWithBroadcastFast import *
from Experiment.Experiment import *
from Util.Util import get_host_ip
seed_map = {
    43: 0,
    248: 100,
    213: 300,
    195: 500,
    207: 700,
    194: 900,
    184: 1100,
    160: 1300,
    225: 1500,
    211: 1700,
    224: 1900}


def IOTAStat(times=1):
    h = open("IOTAStat50246.txt", "w+")
    protocol_list = [IOTA]
    adversary_list = [PossibleAdversaries[8]]
    f_list = [2,4,6]
    node_num = 50
    ip = get_host_ip()
    ip_id = int(ip.split('.')[-1])
    # seed = seed_map[ip_id]
    seed = random.randint(1,10000000000000000)
    _lambda_list=[1]
    RunIOTAExperiment(h, node_num, times, protocol_list,
                      adversary_list, f_list, seed,_lambda_list)
    h.close()
