"""
4 levels of prediction, each level uses more information than the previous one to make prediction.
For input JSON file, "type", "frequency", "row", "column" are necessary for all level of prediction.
"DSP", "BRAM", "LUT", "register" are necessary for level 2 and 3.
"shift_register" is useful for predicting differrent kernel's clock power.
Any additional field does not affect the result.
"""
import json
import math

# Takes in a verbose level, a configuration or a json file containing a configuration
# Output total power, clock power, logic power, BRAM power, DSP power, static power
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

# load a configuration from a json file
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
        if filename == None:
            print("need configuration data or json file")
            exit(1)
        else:
            config = load_config(filename)

    if config["type"] == "Matrix Multiplication":

        # Level 0 is direct linear regression on clock power consumption (#PE vs. clock power)
        if verbose == 0:
            power = 0.07347 * config["PE"] + 1.07316

        # Level 1 is linear regression on fanout, and then regression on power (#PE vs. fanout).
        # Power scales with fanout sublinearly: power = c * fanout ^ x (fanout vs. clock power).
        # C and x are learned from fixed fanout/site and enbale rate.
        # Fanout/site and enable rate are average taken over the training set.
        # The model is learned in XPE: fix fanout/site and enable rate, 
        # input differnt fanout values, and use the input and result power to
        # learn a function with regression tool (such as http://www.xuru.org/rt/).
        elif verbose == 1:
            fanout = 19272.2 + config["PE"] * 8121.5       
            power = 0.0000574704 * math.pow(fanout, 0.8786432479)
        
        # Level 2 estimates fanout as the sum of register, DSP and BRAM.
        # Yhis is 6.4% underestimation because shift register is not considered.
        # The reason shift register is not considered is that shift register is \
        # implemented by LUT, so it is difficult to acquire its quantity. 
        # If shift register number can be obtained, 
        # the program should be modified to include it.
        elif verbose == 2:
            fanout = config["register"] + config["BRAM"] + config["DSP"]
            power = 0.0000574704 * math.pow(fanout, 0.8786432479)

        # Level 3 estimates fanout/site according to the step function \
        # learned from the training set.
        # The change of parameter c and x is due to change of fanout/site
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

    # For other kernels, without prior knowledge, 
    # it is necessary to know the quantity of each component to estimate power
    else:
        if verbose == 1 or verbose == 0:
            print("cannot estimate clock power without #register or prior knowledge")
        else:
            fanout = config["shift_register"] + config["register"] + config["BRAM"] + config["DSP"]
            power = 0.0000574704 * math.pow(fanout, 0.8786432479)

    # Clock power has linear scaling with frequency
    return round(power * config["frequency"] / 333.33333, 4)

def DSP(verbose, config=None, filename=None):
    if config == None:
        if filename == None:
            print("need configuration data or json file")
            exit(1)
        else:
            config = load_config(filename)

    if config["type"] == "Matrix Multiplication":

        # Level 0 is direct linear regression on DSP power consumption (#PE vs. DSP power)
        if verbose == 0:
            power = config["PE"] * 0.04795 - 0.02703 

        # Each PE has 40 DSP (#PE vs. #DSP).
        # DSP has six modes, decided by 3 variables.
        # DSP power is also affected by toggle rate.
        # With fixed toggle rate (set to average of the training set),
        # the average power consumption of 1000 DSP slices of the six modes is 1.1578W (#DSP vs DSP power).
        elif verbose == 1:
            config["DSP"] = config["PE"] * 40
            power = 1.1578 * config["DSP"] / 1000

        # Level 2 number of DSP is given,
        # the result should be exactly the same as level 1 as DSP estimation is accurate.
        elif verbose == 2:
            power = 1.1578 * config["DSP"] / 1000
        
        # Level 3 leverages deeper insight of the kernel. 
        # There are four modes of DSP used in the PE,
        # each with relatively stable toggle rate.
        # This level predicts each modes of DSP separately.
        else:
            # 20% of the DSPs do not use multiply or pre-add
            DSP1 = 0.779 * config["DSP"] / 5000
            # 20% of the DSPs use multiply but not MREG or pre-add
            DSP2 = 1.222 * config["DSP"] / 5000
            # 40% of the DSPs use multiply and MREG but not pre-add
            DSP3 = 1.117 * config["DSP"] / 2500
            # 20% of the DSPs use mulitply, MREG and pre-add
            DSP4 = 1.576 * config["DSP"] / 5000
            power = DSP1 + DSP2 + DSP3 + DSP4

    # For other kernels, without prior knowledge, 
    # it is necessary to know the quantity of DSPs to estimate power       
    else:
        if verbose == 1 or verbose == 0:
            print("cannot estimate DSP power without #DSP or prior knowledge")
        else:
            power = 1.1578 * config["DSP"] / 1000

    # DSP power has linear scaling with frequency
    return round(power * config["frequency"] / 333.33333, 4)

# Logic includes LUT and register
def logic(verbose, config=None, filename=None):
    if config == None:
        if filename == None:
            print("need configuration data or json file")
            exit(1)
        else:
            config = load_config(filename)

    if config["type"] == "Matrix Multiplication":

        # Level 0 is direct linear regression on logic power consumption (#PE vs. logic power)
        if verbose == 0:
            power = config["PE"] * 0.12061 + 0.15987

        # Level 1 first predicts the amount of LUTs and registers used (#PE vs #LUT and #register),
        # then predicts the power usage (#LUT and #register vs. LUT and register power).
        # With fixed toggle rate and routing complexity (set to average of the most common type of LUT used in training set),
        # the average power consumption of 10000 LUTs is 0.1221W, 10000 registers is 0.0670W.
        elif verbose == 1:
            config["LUT"] = 4302.84 * config["PE"] + 9697.9
            config["register"] = 7580.17 * config["PE"] + 18682.2
            lut = 0.1221 * config["LUT"] / 10000
            reg = 0.0670 * config["register"] / 10000
            power = lut + reg
        
        # Level 2 directly use number of LUTs and registers
        elif verbose == 2:
            lut = 0.1221 * config["LUT"] / 10000
            reg = 0.0670 * config["register"] / 10000
            power = lut + reg

        # The total LUTs used are split in three categories.
        # In average 89.13% of them are used as logic with lower complexity,
        # 10.54% are used as FIFO, and 0.33% used as logic with high complexity.
        # 99.4% of the registers have low complexity, the rest have high complexity.
        # Obvisouly, level 3's result should be higher than level 2's,
        # because level 2 assume all LUTs and registers used are the common type, 
        # while in reality some of them consume higher power.
        else:
            logic1 = config["LUT"] * 0.1221 * 0.8913 / 10000
            fifo = config["LUT"] * 0.1856 * 0.1054 / 10000
            logic2 = config["LUT"] * 1.5803 * 0.0033 / 10000
            reg1 = config["register"] * 0.0670 * 0.9940 / 10000
            reg2 = config["register"] * 1.5767 * 0.0060 / 10000
            
            power = logic1 + fifo + logic2 + reg1 + reg2

    # For other kernels, without prior knowledge, 
    # it is necessary to know the quantity of LUTs and registers to estimate power  
    else:
        if verbose == 1 or verbose == 0:
            print("cannot estimate logic power without #logic or prior knowledge")
        else:
            lut = 0.1221 * config["LUT"] / 10000
            reg = 0.0670 * config["register"] / 10000
            power = lut + reg

    # logic power has linear scaling with frequency
    return round(power * config["frequency"] / 333.33333,4)

def BRAM(verbose, config=None, filename=None):
    if config == None:
        if filename == None:
            print("need configuration data or json file")
            exit(1)
        else:
            config = load_config(filename)

    if config["type"] == "Matrix Multiplication":

        # Level 0 is direct linear regression on logic power consumption. (#PE vs. BRAM power)
        if verbose == 0:
            power = config["PE"] * 0.00687 + 0.55597

        # Level 1 first predicts the amount of BRAMs used,
        # then predicts the power usage.
        # BRAM usage model is linear regression on traning set (#PE vs. #BRAM)
        # Power usage model is also linear regression on training set (#BRAM vs. BRAM power)
        # This two-step linear regression may introduce over-fitting compared to level 0's direct linear regression.
        elif verbose == 1:
            config["BRAM"] = 3.1568 * config["PE"] + 134.7834
            power = 0.002175 * config["BRAM"] + 0.262823
        # Level 2 directly uses number of BRAM
        # There is no further insight so level 3 is the same as level 2.
        else:
            power = 0.002175 * config["BRAM"] + 0.262823

    # For other kernels, without prior knowledge, 
    # it is necessary to know the quantity of BRAMs to estimate power  
    else:
        if verbose == 1 or verbose == 0:
            print("cannot estimate BRAM power without #BRAM or prior knowledge")
        else:
            power = 0.00191 * config["BRAM"] + 0.327554

    # BRAM power has linear scaling with frequency
    return round(power * config["frequency"] / 333.33333, 4)

def static(verbose, config=None, filename=None):
    if config == None:
        config = load_config(filename)
    
    # Static power scales linearly with #PE, but very slowly (#PE vs. static power)
    power = 0.004574 * config["PE"] + 2.493541
    return round(power * config["frequency"] / 333.33333, 4)

if __name__ == "__main__":
    power(2, None, "example.json")