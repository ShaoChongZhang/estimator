import sys
import os
import csv
import numpy

# input the number of points for the regression and the data file (power_data.csv)
# output the average error rate and variance of linear regerssion from every combination of points 
def regression(points, filename):
    csvfile = []
    with open(filename, mode='r', newline='') as one:
        reader = csv.reader(one, delimiter=',', quotechar='|')
        # read the input file into a list
        for row in reader:
            csvfile.append([float(item) for item in row])
    # check if there are enough entries in the list for the regerssion
    if len(csvfile) < points:
        print("cannot perform linear regression: too few data points")
        exit(0)
    

    with open(str(points) + '_point_result.csv', 'w', newline='') as result:
        writer = csv.writer(result, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # list of entries for linear regression
        regression_list = [0] * points
        recursive(points, 0, csvfile, writer, regression_list)

# a n-level nested loop (n is the number of points), implemented in recursion
def recursive(points, level, csvfile, writer, regression_list):
    # the first level of recursion
    if level == 0:
        for i in range(0, len(csvfile)):
            regression_list[level] = i
            recursive(points, level+1, csvfile, writer, regression_list)
    # neither the first nor the last level of recursion
    elif level != points:
        # for the next point to add to the regression list,
        # only consider entries bigger than the previous one in the list to avoid duplicated combination
        for i in range(regression_list[level-1]+1, len(csvfile)):
            regression_list[level] = i
            recursive(points, level+1, csvfile, writer, regression_list)
    # last level of recursion
    # regression_list is filled, now for the calculation
    else:
        # list of number of PE
        pe_list = []
        for entry in regression_list:
            pe_list.append(csvfile[entry][2])
        # take out combinations that have multiple points with same number of PE
        pe_list_sort = sorted(pe_list)
        for i in range (0, len(pe_list)-1):
            if pe_list_sort[i] == pe_list_sort[i+1]:
                return None
        
        # list of power
        power_list = []
        for entry in regression_list:
            power_list.append(csvfile[entry][8])
        
        # for one point regression, add the origin point for regression
        if points == 1:
            pe_list.append(0)
            power_list.append(0.0)
        
        # linear regression of the points,
        # output coefficient and intercept
        linear_regression = numpy.polyfit(pe_list, power_list, 1)
        coefficient = linear_regression[0]
        intercept = linear_regression[1]

        # compute the error rate of each point against the model
        error = [0.0] * len(csvfile)
        for i in range(0, len(csvfile)):
            if i not in regression_list:
                error[i] = abs(csvfile[i][8] - coefficient * csvfile[i][2] - intercept) / csvfile[i][8]
        
        # compute average error rate
        average_error = sum(error) / (len(csvfile) - points)

        # compute the variance of error rate
        variance = 0.0
        for i in range(0, len(csvfile)):
            if i not in regression_list:
                variance += (error[i] - average_error) * (error[i] - average_error) / (len(csvfile) - points)
        
        # print result to file
        newrow = []
        for entry in regression_list:
            newrow.append(csvfile[entry][0])
            newrow.append(csvfile[entry][1])
        newrow.append(average_error)
        newrow.append(variance)
        writer.writerow(newrow)

if __name__ == "__main__":
    regression(int(sys.argv[1]), sys.argv[2])