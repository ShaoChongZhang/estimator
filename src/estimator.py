import json
import math

ClockEnable = 0.305858
FanoutPerSite = 3.040281
DSPToggle = 9.720727

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
    print(clock_power)
    print(logic_power)
    print(BRAM_power)
    print(DSP_power)
    print(clock_power + BRAM_power + DSP_power + logic_power)
    return clock_power + BRAM_power + DSP_power + logic_power


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
            fanout = 18080.5 + config["PE"] * 8126.03
            power = 0.000057768 * math.pow(fanout, 0.878646)
        elif verbose == 2:
            fanout = config["register"] + config["BRAM"] + config["DSP"]
            power = 0.000057768 * math.pow(fanout, 0.878646)
        else:
            fanout = config["register"] + config["BRAM"] + config["DSP"]
            if config["PE"] > 46:
                power = 0.0000523458 * math.pow(fanout, 0.880098)
            elif config["PE"] > 29:
                power = 0.0000566314 * math.pow(fanout, 0.878934)
            elif config["PE"] > 16:
                power = 0.0000593269 * math.pow(fanout, 0.878313)
            elif config["PE"] > 11:
                power = 0.0000669245 * math.pow(fanout, 0.876658)
            else:
                power = 0.0000721758 * math.pow(fanout, 0.875768)
    else:
        if verbose == 1:
            print("cannot estimate clock power without #register or prior knowledge")
        else:
            fanout = config["shift_register"] + config["register"] + config["BRAM"] + config["DSP"]
            power = 0.0000577676 * math.pow(fanout, 0.878646)

    return power * config["frequency"] / 333.33333

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
            power = 1.15783 * config["DSP"] / 1000

    return power * config["frequency"] / 333.33333


def logic(verbose, config=None, filename=None):
    if config == None:
        config = load_config(filename)

    if config["type"] == "Matrix Multiplication":
        if verbose == 1:
            lut = 4298.17 * config["PE"] + 9191.8
            reg = 7584.22 * config["PE"] + 17578.5
            lut = 0.1221 * lut / 10000
            reg = 0.0671 * reg / 10000
            power = lut + reg
        elif verbose == 2:
            lut = 0.1221 * config["LUT"] / 10000
            reg = 0.0671 * config["register"] / 10000
            power = lut + reg
        else:
            lut1 = 0.1221 * 0.8909 * config["LUT"] / 10000
            lut2 = 0.1859 * 0.0031 * config["LUT"] / 10000
            lut3 = 1.6399 * 0.106 * config["LUT"] / 10000
            reg1 = 0.0671 * 0.994 * config["register"] / 10000
            reg2 = 1.6362 * 0.006 * config["register"] / 10000
            
            power = lut1 + lut2 + lut3 + reg1 + reg2
    else:
        if verbose == 1:
            print("cannot estimate logic power without #logic or prior knowledge")
        else:
            lut = 0.1221 * config["LUT"] / 10000
            reg = 0.0671 * config["register"] / 10000
            power = lut + reg

    return power * config["frequency"] / 333.33333

def BRAM(verbose, config=None, filename=None):
    if config == None:
        config = load_config(filename)

    if config["type"] == "Matrix Multiplication":
        if verbose == 1:
            power = 0.0069894 * config["PE"] + 0.549718
        else:
            power = 0.00294597 * config["BRAM"]
    else:
        if verbose == 1:
            print("cannot estimate logic power without #logic or prior knowledge")
        else:
            power = 0.00294597 * config["BRAM"]

    return power * config["frequency"] / 333.33333

if __name__ == "__main__":
    power(2, None, "example.json")