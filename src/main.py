import json
import csv
import sys
import estimator as es

test_set = [43, 34, 8, 29, 18, 53, 30, 5, 38, 21, 20, 3, 13, 26, 41, 1]

def main(verbose, argv):
    verbose = int(verbose)
    if verbose < 1 or verbose > 3:
        print("verbose level must be one of 1, 2, 3")
        exit(1)
    for file in argv:
        config = es.load_config(file)
        power = es.power(verbose, config)
        print("total: " + str(power[0]))
        print("clock: " + str(power[1]))
        print("logic: " + str(power[2]))
        print("BRAM: " + str(power[3]))
        print("DSP: " + str(power[4]))
        print("static: " + str(power[5]))

def estimate_all(path):
    with open('result_train_1.csv', 'w', newline='') as train1, open('result_test1.csv', 'w', newline='') as test1, \
        open('result_train_2.csv', 'w', newline='') as train2, open('result_test2.csv', 'w', newline='') as test2, \
        open('result_train_3.csv', 'w', newline='') as train3, open('result_test3.csv', 'w', newline='') as test3:

        writer_train1 = csv.writer(train1, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test1 = csv.writer(test1, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_train2 = csv.writer(train2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test2 = csv.writer(test2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_train3 = csv.writer(train3, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test3 = csv.writer(test3, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(path + "/" + str(i) + "x" + str(j) + ".json", "r") as f:
                        config = json.load(f)
                        config["PE"] = config["row"] * config["column"]
                        power = es.power(1, config)
                        if count in test_set:
                            writer_test1.writerow([i, j, i * j, power[1], power[2], power[3], power[4], power[5], power[1] + power[2] + power[3] + power[4], power[0]])
                        else:
                            writer_train1.writerow([i, j, i * j, power[1], power[2], power[3], power[4], power[5], power[1] + power[2] + power[3] + power[4], power[0]])
                        power = es.power(2, config)
                        if count in test_set:
                            writer_test2.writerow([i, j, i * j, power[1], power[2], power[3], power[4], power[5], power[1] + power[2] + power[3] + power[4], power[0]])
                        else:
                            writer_train2.writerow([i, j, i * j, power[1], power[2], power[3], power[4], power[5], power[1] + power[2] + power[3] + power[4], power[0]])
                        power = es.power(3, config)
                        if count in test_set:
                            writer_test3.writerow([i, j, i * j, power[1], power[2], power[3], power[4], power[5], power[1] + power[2] + power[3] + power[4], power[0]])
                        else:
                            writer_train3.writerow([i, j, i * j, power[1], power[2], power[3], power[4], power[5], power[1] + power[2] + power[3] + power[4], power[0]])
                        count += 1
                except FileNotFoundError:
                    pass


if __name__ == "__main__":
    """
    main(sys.argv[1], sys.argv[2:])
    """
    estimate_all(sys.argv[1])