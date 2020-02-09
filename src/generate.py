import json
import sys

def main(argv):
    design = {}
    design["type"] = "Matrix Multiplication"
    design["verbose"] = 2
    design["frequency"] = 333.33333
    design["row"] = 4
    design["column"] = 4
    design["input row"] = 128
    design["input column"] = 128
    design["LUT"] = 79802
    design["register"] = 137770
    design["DSP"] = 640
    design["BRAM"] = 169
    design["URAM"] = 0
    design["logic"] = 71825
    design["shift register"] = 7977
    design["dsitributed RAM"] = 0

    
    with open(argv[0], "w") as f:
        json.dump(design, f, indent=2)

if __name__ == "__main__":
    main(sys.argv[1:])