import json
import sys

def main(argv):
    design = {}
    design["type"] = "Matrix Multiplication"
    design["verbose"] = 2
    design["frequency"] = 333.33333
    design["row"] = 4
    design["column"] = 4
    design["inputX"] = 128
    design["inputY"] = 128
    design["inputZ"] = 128
    design["DSP"] = 640
    design["BRAM"] = 169
    design["URAM"] = 0
    design["LUT"] = 79802
    design["register"] = 137770
    
    with open(argv[0], "w") as f:
        json.dump(design, f, indent=2)

if __name__ == "__main__":
    main(sys.argv[1:])