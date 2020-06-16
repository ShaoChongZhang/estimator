import json
import math

def power(verbose, config=None, filename=None):
    if config == None:
        if filename == None:
            print("config needed")
            exit(1)
        else:
            config = load_config(filename)

    clock_power = clock(verbose,config)
    logic_power = logic(verbose, config)
    BRAM_power = BRAM(verbose, config)
    DSP_power = DSP(verbose, config)
    static_power = static(verbose, config)
    
    return round(clock_power + BRAM_power + DSP_power + logic_power + static_power, 3), clock_power, logic_power, BRAM_power, DSP_power, static_power


def load_config(filename):
    try:
        with open(filename, "r") as f:
            config = json.load(f)
            config["PE"] = config["row"] * config["column"]

    except:
        print("file " + filename + " cannot be opened")
        exit(1)
    
    return config

def clock(verbose, config=None, filename=None):
    if config == None:
        config = load_config(filename)

    if config["type"] == "Matrix Multiplication":
        if verbose == 1:
            fanout = 19272.2 + config["PE"] * 8121.5       
            power = 0.0000574704 * math.pow(fanout, 0.8786432479)
        elif verbose == 2:
            fanout = config["register"] + config["BRAM"] + config["DSP"]
            power = 0.0000574704 * math.pow(fanout, 0.8786432479)
        else:
            fanout = config["register"] + config["BRAM"] + config["DSP"]
            if config["PE"] > 46:
                power = 0.0000523526 * math.pow(fanout, 0.8800554742)
            elif config["PE"] > 29:
                power = 0.0000566359 * math.pow(fanout, 0.8788793843)
            elif config["PE"] > 16:
                power = 0.0000593380 * math.pow(fanout, 0.8782739659)
            elif config["PE"] > 11:
                power = 0.0000669248 * math.pow(fanout, 0.8766213742)
            else:
                power = 0.0000721882 * math.pow(fanout, 0.875725741)
    else:
        if verbose == 1:
            print("cannot estimate clock power without #register or prior knowledge")
        else:
            fanout = config["shift_register"] + config["register"] + config["BRAM"] + config["DSP"]
            power = 0.0000574704 * math.pow(fanout, 0.8786432479)

    return round(power * config["frequency"] / 333.33333, 4)

def DSP(verbose, config=None, filename=None):
    if config == None:
        config = load_config(filename)

    if config["type"] == "Matrix Multiplication":
        if verbose == 1:
            config["DSP"] = config["PE"] * 40
            power = 1.1578 * config["DSP"] / 1000
        elif verbose == 2:
            power = 1.1578 * config["DSP"] / 1000
        else:
            DSP1 = 0.779 * config["DSP"] / 5000
            DSP2 = 1.222 * config["DSP"] / 5000
            DSP3 = 1.117 * config["DSP"] / 2500
            DSP4 = 1.576 * config["DSP"] / 5000
            power = DSP1 + DSP2 + DSP3 + DSP4
    else:
        if verbose == 1:
            print("cannot estimate DSP power without #DSP or prior knowledge")
        else:
            power = 1.1578 * config["DSP"] / 1000

    return round(power * config["frequency"] / 333.33333, 4)


def logic(verbose, config=None, filename=None):
    if config == None:
        config = load_config(filename)

    if config["type"] == "Matrix Multiplication":
        if verbose == 1:
            config["LUT"] = 4302.84 * config["PE"] + 9697.9
            config["register"] = 7580.17 * config["PE"] + 18682.2
            lut = 0.1221 * config["LUT"] / 10000
            reg = 0.0670 * config["register"] / 10000
            power = lut + reg
        elif verbose == 2:
            lut = 0.1221 * config["LUT"] / 10000
            reg = 0.0670 * config["register"] / 10000
            power = lut + reg
        else:
            logic1 = config["LUT"] * 0.1221 * 0.8913 / 10000
            fifo = config["LUT"] * 0.1856 * 0.1054 / 10000
            logic2 = config["LUT"] * 1.5803 * 0.0033 / 10000
            reg1 = config["register"] * 0.0670 * 0.9940 / 10000
            reg2 = config["register"] * 1.5767 * 0.0060 / 10000
            
            power = logic1 + fifo + logic2 + reg1 + reg2
    else:
        if verbose == 1:
            print("cannot estimate logic power without #logic or prior knowledge")
        else:
            lut = 0.1221 * config["LUT"] / 10000
            reg = 0.0670 * config["register"] / 10000
            power = lut + reg

    return round(power * config["frequency"] / 333.33333,4)

def BRAM(verbose, config=None, filename=None):
    if config == None:
        config = load_config(filename)

    if config["type"] == "Matrix Multiplication":
        if verbose == 1:
            config["BRAM"] = 3.1568 * config["PE"] + 134.7834
            power = 0.002175 * config["BRAM"] + 0.262823
        else:
            power = 0.00191 * config["BRAM"] + 0.327554
    else:
        if verbose == 1:
            print("cannot estimate BRAM power without #BRAM or prior knowledge")
        else:
            power = 0.00191 * config["BRAM"] + 0.327554

    return round(power * config["frequency"] / 333.33333, 4)

def static(verbose, config=None, filename=None):
    if config == None:
        config = load_config(filename)
    power = 0.004574 * config["PE"] + 2.493541
    return round(power * config["frequency"] / 333.33333, 4)

if __name__ == "__main__":
    power(2, None, "example.json")