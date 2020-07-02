"""
This script parse the .xpe power report files,
and turn them into json files for estimator.
"""

import sys
import os
import csv
import json
import re

patternclock = "				<CLOCK name=\"ap_clk\" freq=\"333.333330\" belFanout=\"(.*)\" sliceFanout=\"(.*)\" FoPerSite=\"(.*)\" sliceEnableRate=\"(.*)\" leafs+"
patternlogic1 = "				<LOGIC clock=\"Unclocked_or_HFN_instance\" clockFreq=\"333.333330\" clockFreq2=\"333.333330\" toggleRate=\"(.*)\" toggleRate2=\"(.*)\" totalRate=\"(.*)\" name=\"ap_clk\" hierName=\"bd_0_wrapper/bd_0_i\" writeRate=\"0.000000\" enableRate=\"0.000000\" fanout=\"(.*)\" ru=\"(.*)\" fanout2=\"(.*)\" totalFanout=\"(.*)\" fanoutRate=\"(.*)\" numNets=\"(.*)\" extNets=\"(.*)\" SMUX=\"(.*)\" carry8s=\"(.*)\" luts=\"(.*)\" logicCap=+"
patternlogic2 = "				<LOGIC clock=\"ap_clk\" clockFreq=\"333.333330\" clockFreq2=\"333.333330\" toggleRate=\"(.*)\" toggleRate2=\"(.*)\" totalRate=\"(.*)\" name=\"ap_clk\" hierName=\"bd_0_wrapper/bd_0_i\" writeRate=\"0.000000\" enableRate=\"(.*)\" fanout=\"(.*)\" ru=\"(.*)\" fanout2=\"(.*)\" totalFanout=\"(.*)\" fanoutRate=\"(.*)\" numNets=\"(.*)\" extNets=\"(.*)\" SRL=\"(.*)\" logicCap+"
patternlogic3 = "				<LOGIC clock=\"ap_clk\" clockFreq=\"333.333330\" clockFreq2=\"333.333330\" toggleRate=\"(.*)\" toggleRate2=\"(.*)\" totalRate=\"(.*)\" name=\"ap_clk\" hierName=\"bd_0_wrapper/bd_0_i\" writeRate=\"0.000000\" enableRate=\"(.*)\" fanout=\"(.*)\" ru=\"(.*)\" fanout2=\"(.*)\" totalFanout=\"(.*)\" fanoutRate=\"(.*)\" numNets=\"(.*)\" extNets=\"(.*)\" ffs=\"(.*)\" logicCap+"
patternlogic4 = "				<LOGIC clock=\"Unclocked_or_HFN_instance\" clockFreq=\"333.333330\" clockFreq2=\"(.*)\" toggleRate=\"(.*)\" toggleRate2=\"(.*)\" totalRate=\"(.*)\" name=\"High_Fanout_Nets\" hierName=\"bd_0_wrapper/bd_0_i\" writeRate=\"0.000000\" enableRate=\"(.*)\" fanout=\"(.*)\" ru=\"(.*)\" fanout2=\"(.*)\" totalFanout=\"(.*)\" fanoutRate=\"(.*)\" numNets=\"(.*)\" extNets=\"(.*)\" carry8s=\"(.*)\" ffs=\"(.*)\" luts=\"(.*)\" logicCap+"
patternDSP1 = "(.*)toggleRate=\"(.*)\" clockFreq=\"333.333330\" multUsed=\"No\" mregUsed=\"No\" preAdderUsed=\"No\" power=\"(.*)\">"
patternDSP2 = "(.*)toggleRate=\"(.*)\" clockFreq=\"333.333330\" multUsed=\"Yes\" mregUsed=\"No\" preAdderUsed=\"No\" power+"
patternDSP3 = "(.*)toggleRate=\"(.*)\" clockFreq=\"333.333330\" multUsed=\"Yes\" mregUsed=\"Yes\" preAdderUsed=\"No\" power+"
patternDSP4 = "(.*)toggleRate=\"(.*)\" clockFreq=\"333.333330\" multUsed=\"Yes\" mregUsed=\"Yes\" preAdderUsed=\"Yes\" power+"
patternBRAM1 = "(.*)count=\"(.*)\">"
patternBRAM2 = "(.*)mode=\"(.*)\" cascade+"
test_set = [43, 34, 8, 29, 18, 53, 30, 5, 38, 21, 20, 3, 13, 26, 41, 1]

def clock():
    with open('clock_train.csv', 'w', newline='') as train, open('clock_test.csv', 'w', newline='') as test:
        writer_train = csv.writer(train, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(test, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                        for line in f:
                            m = re.match(patternclock, line)
                            if m:
                                fanout = m.group(1)
                                fanoutPerSite = m.group(3)
                                enable = m.group(4)
                                if count in test_set:
                                    writer_test.writerow([i, j, i * j, fanout, fanoutPerSite, enable])
                                else:
                                    writer_train.writerow([i, j, i * j, fanout, fanoutPerSite, enable])
                                count += 1
                            

                except FileNotFoundError:
                    pass

def logic1():
    with open('logic1_train.csv', 'w', newline='') as train, open('logic1_test.csv', 'w', newline='') as test:
        writer_train = csv.writer(train, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(test, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                        for line in f:
                            m = re.match(patternlogic1, line)
                            if m:
                                togglerate = m.group(1)
                                complexity = m.group(5)
                                logic1 = m.group(13)
                                if count in test_set:
                                    writer_test.writerow([i, j, i * j, togglerate, complexity, logic1])
                                else:
                                    writer_train.writerow([i, j, i * j, togglerate, complexity, logic1])
                                count += 1

                except FileNotFoundError:
                    pass

def logic2():
    with open('logic2_train.csv', 'w', newline='') as train, open('logic2_test.csv', 'w', newline='') as test:
        writer_train = csv.writer(train, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(test, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                        for line in f:
                            m = re.match(patternlogic2, line)
                            if m:
                                togglerate = m.group(1)
                                complexity = m.group(6)
                                ff = m.group(12)
                                if count in test_set:
                                    writer_test.writerow([i, j, i * j, togglerate, complexity, ff])
                                else:
                                    writer_train.writerow([i, j, i * j, togglerate, complexity, ff])
                                count += 1

                except FileNotFoundError:
                    pass

def logic3():
    with open('logic3_train.csv', 'w', newline='') as train, open('logic3_test.csv', 'w', newline='') as test:
        writer_train = csv.writer(train, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(test, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                        for line in f:
                            m = re.match(patternlogic3, line)
                            if m:
                                togglerate = m.group(1)
                                complexity = m.group(6)
                                reg = m.group(12)
                                if count in test_set:
                                    writer_test.writerow([i, j, i * j, togglerate, complexity, reg])
                                else:
                                    writer_train.writerow([i, j, i * j, togglerate, complexity, reg])
                                count += 1

                except FileNotFoundError:
                    pass

def logic4():
    with open('logic4_train.csv', 'w', newline='') as train, open('logic4_test.csv', 'w', newline='') as test:
        writer_train = csv.writer(train, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(test, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                        for line in f:
                            m = re.match(patternlogic4, line)
                            if m:
                                togglerate = m.group(2)
                                complexity = m.group(7)
                                ff = m.group(14)
                                luts = m.group(15)
                                if count in test_set:
                                    writer_test.writerow([i, j, i * j, togglerate, complexity, luts, ff])
                                else:
                                    writer_train.writerow([i, j, i * j, togglerate, complexity, luts, ff])
                                count += 1

                except FileNotFoundError:
                    pass

def DSP1():
    with open('DSP1_train.csv', 'w', newline='') as train, open('DSP1_test.csv', 'w', newline='') as test:
        writer_train = csv.writer(train, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(test, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                        for line in f:
                            m = re.match(patternDSP1, line)
                            if m:
                                togglerate = m.group(2)
                                if count in test_set:
                                    writer_test.writerow([i, j, i * j, togglerate])
                                else:
                                    writer_train.writerow([i, j, i * j, togglerate])
                                count += 1

                except FileNotFoundError:
                    pass

def DSP2():
    with open('DSP2_train.csv', 'w', newline='') as train, open('DSP2_test.csv', 'w', newline='') as test:
        writer_train = csv.writer(train, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(test, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                        for line in f:
                            m = re.match(patternDSP2, line)
                            if m:
                                togglerate = m.group(2)
                                if count in test_set:
                                    writer_test.writerow([i, j, i * j, togglerate])
                                else:
                                    writer_train.writerow([i, j, i * j, togglerate])
                                count += 1

                except FileNotFoundError:
                    pass

def DSP3():
    with open('DSP3_train.csv', 'w', newline='') as train, open('DSP3_test.csv', 'w', newline='') as test:
        writer_train = csv.writer(train, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(test, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                        for line in f:
                            m = re.match(patternDSP3, line)
                            if m:
                                togglerate = m.group(2)
                                if count in test_set:
                                    writer_test.writerow([i, j, i * j, togglerate])
                                else:
                                    writer_train.writerow([i, j, i * j, togglerate])
                                count += 1

                except FileNotFoundError:
                    pass

def DSP4():
    with open('DSP4_train.csv', 'w', newline='') as train, open('DSP4_test.csv', 'w', newline='') as test:
        writer_train = csv.writer(train, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(test, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                        for line in f:
                            m = re.match(patternDSP4, line)
                            if m:
                                togglerate = m.group(2)
                                if count in test_set:
                                    writer_test.writerow([i, j, i * j, togglerate])
                                else:
                                    writer_train.writerow([i, j, i * j, togglerate])
                                count += 1

                except FileNotFoundError:
                    pass

def BRAM():
    with open('BRAM_train.csv', 'w', newline='') as train, open('BRAM_test.csv', 'w', newline='') as test:
        writer_train = csv.writer(train, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer_test = csv.writer(test, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        count = 1
        for i in range(2, 9):
            for j in range(2, 14):
                try:
                    with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                        RAMB18 = 0
                        RAMB36 = 0
                        RAMB18SDP = 0
                        RAMB36SDP = 0
                        cnt = 0
                        for line in f:
                            m = re.match(patternBRAM1, line)
                            if m:
                                cnt = m.group(2)
                            n = re.match(patternBRAM2, line)
                            if n:
                                ram = n.group(2)
                                if ram == "RAMB36":
                                    RAMB36 += int(cnt)
                                elif ram == "RAMB18":
                                    RAMB18 += int(cnt)
                                elif ram == "RAMB36SDP":
                                    RAMB36SDP += int(cnt)
                                elif ram == "RAMB18SDP":
                                    RAMB18SDP += int(cnt)
                        if count in test_set:
                            writer_test.writerow([i, j, i * j, RAMB18, RAMB18SDP, RAMB36, RAMB36SDP])
                        else:
                            writer_train.writerow([i, j, i * j, RAMB18, RAMB18SDP, RAMB36, RAMB36SDP])
                        count += 1

                except FileNotFoundError:
                    pass

def create_json():
    for i in range(2, 9):
        for j in range(2, 14):
            try:
                logic1 = 0
                logic2 = 0
                ff = 0
                reg1 = 0
                reg2 = 0
                with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                    for line in f:
                        m = re.match(patternlogic1, line)
                        if m:
                            logic1 = m.group(13)
                with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                    for line in f:
                        m = re.match(patternlogic2, line)
                        if m:
                            ff = m.group(12)
                with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                    for line in f:
                        m = re.match(patternlogic3, line)
                        if m:
                            reg1 = m.group(12)
                with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                    for line in f:
                        m = re.match(patternlogic4, line)
                        if m:
                            reg2 = m.group(14)
                            logic2 = m.group(15)
                

                    
                cnt = 0
                cct = 0
                with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                    for line in f:
                        m = re.match(patternBRAM1, line)
                        if m:
                            cnt = m.group(2)
                        n = re.match(patternBRAM2, line)
                        if n:
                            ram = n.group(2)
                            if ram == "RAMB36":
                                cct += int(cnt)
                            elif ram == "RAMB18":
                                cct += int(cnt)
                            elif ram == "RAMB36SDP":
                                cct += int(cnt)
                            elif ram == "RAMB18SDP":
                                cct += int(cnt)
                with open(str(i) + "x" + str(j) + "\\" + str(i) + "x" + str(j) + ".xpe") as f:
                    luts = int(logic1) + int(logic2) + int(ff)
                    regs = int(reg1) + int(reg2)
                    design = {}
                    design["type"] = "Matrix Multiplication"
                    design["frequency"] = 333.33333
                    design["row"] = i
                    design["column"] = j
                    design["inputX"] = 128
                    design["inputY"] = 128
                    design["inputZ"] = 128
                    design["DSP"] = i * j * 40
                    design["BRAM"] = cct
                    design["URAM"] = 0
                    design["LUT"] = luts
                    design["register"] = regs
    
                    with open(str(i) + "x" + str(j) + ".json", "w") as j:
                        json.dump(design, j, indent=2)   

            except FileNotFoundError:
                pass

if __name__ == "__main__":
    
    clock()
    BRAM()
    