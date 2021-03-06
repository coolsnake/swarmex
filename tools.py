import logging
import logging.config
import pickle
import os
import json

def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


from fitness import Fitness

def calculate_average_fitness(tfitnesses, log_path):
    
    Avalue = 0
    Au_sell= 0
    Au_buy= 0
    Anoop= 0
    Arealised_profit= 0
    Amdd= 0
    Aret= 0
    Awealth= 0
    Ano_of_transactions= 0
    n_runs = len(tfitnesses)

    for f in tfitnesses:
        Avalue += tfitnesses[f].value
        Au_sell += tfitnesses[f].u_sell
        Au_buy += tfitnesses[f].u_buy
        Anoop += tfitnesses[f].noop
        Arealised_profit += tfitnesses[f].realised_profit
        Amdd += tfitnesses[f].mdd
        Aret += tfitnesses[f].ret
        Awealth += tfitnesses[f].wealth
        Ano_of_transactions += tfitnesses[f].no_of_transactions

    Af = Fitness(value= Avalue / n_runs,
                u_sell= Au_sell / n_runs,
                u_buy= Au_buy / n_runs,
                noop= Anoop / n_runs,
                realised_profit= Arealised_profit / n_runs,
                mdd= Amdd / n_runs,
                ret= Aret / n_runs,
                wealth= Awealth / n_runs,
                no_of_transactions= Ano_of_transactions / n_runs)
    
    open(log_path + 'results.txt', 'w').close()
    with open(log_path + 'results.txt', 'a') as f:
        f.write("number of runs\tavg wealth\tavg return\tavg value\tavg profit\tavg mdd\tavg transactions\tavg short transactions\n")
        f.write("%d\t%s" % (n_runs, Af))
        print("Average fitness: %s" % Af)
    pickle.dump(Af.__dict__, open(log_path+"pickles/average_fitness.pickle", "wb" ) )


import socket, errno
def socket_is_free(port):
     # check if socket is available
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            s.close()
            return False
        else:
            # something else raised the socket.error exception
            s.close()
            print(e)
            return False
    s.close()
    return True
