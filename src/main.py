import json
import sys
import estimator as es

def main(argv):
    for file in argv:
        config = es.load_config(file)
        power = es.power(config)
        print(power)

if __name__ == "__main__":
    main(sys.argv[1:])