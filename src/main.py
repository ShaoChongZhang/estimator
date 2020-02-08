import json
import sys
import estimator as es

def main(argv):
    try:
        with open(argv[0], "r") as f:
            configuration = json.load(f)
    except FileNotFoundError:
        print("file " + argv[0] + " not found")
        exit(1)
    
    power = es.Estimator(configuration)
    power.printResult()

if __name__ == "__main__":
    main(sys.argv[1:])