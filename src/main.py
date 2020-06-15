import json
import sys
import estimator as es

def main(verbose, argv):
    verbose = int(verbose)
    if verbose < 1 or verbose > 3:
        print("verbose level must be one of 1, 2, 3")
        exit(1)
    for file in argv:
        config = es.load_config(file)
        power = es.power(verbose, config)
        print("total: " + str(power))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])