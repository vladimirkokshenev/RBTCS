import xlrd
import xlwt
import argparse
import sys
import os.path
import logging
import enum

default_arguments = {"rbtcs": "rbtcs.py",
                     "filename": "testcases.xls",
                     "risk factor": "Risk Factor",
                     "execution time": "Execution Time",
                     "selection": "Selected",
                     "time budget": 2500,
                     "logger": "rbtcs"}

status_code = enum.Enum('OK',
                        'ERR_FILE_NOT_FOUND',
                        'ERR_XLRD_READ',
                        'ERR_RISK_FACTOR_NOT_FOUND',
                        'ERR_EXECUTION_TIME_NOT_FOUND',
                        'ERR_SELECTION_NOT_FOUND',
                        'ERR_TIME_BUDGET_NOT_POSITIVE',
                        'ERR_RISK_FACTOR_TYPE',
                        'ERR_EXECUTION_TIME_TYPE')

MAX_BUDGET = 10000
MAX_TC = 300

def init_logger():
    """ Initialize logger: set logging level, logging message format and handler """

    logger = logging.getLogger(default_arguments["logger"])
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


def parse_arguments(arguments):
    """ Validate input filename.

    :param arguments: sys.argv structure with input arguments
    :return: parsed argument in a structure returned by parser.parse_args()
    """

    parser = argparse.ArgumentParser(description="Risk-Based Test Case Selector Tool")

    parser.add_argument("filename",
                        default=default_arguments["filename"],
                        help="the seed file with test cases (xls/xlsx)")

    parser.add_argument("--risk-factor",
                        default=default_arguments["risk factor"],
                        help="the column name containing risk factor of a test case (def=Risk Factor)",
                        dest="risk_factor")

    parser.add_argument("--execution-time",
                        default=default_arguments["execution time"],
                        help="the column name containing execution time of a test case (def=Execution Time)",
                        dest="execution_time")

    parser.add_argument("--selection",
                        default=default_arguments["selection"],
                        help="the column name with a test case selection into resulting test set (def=Selected)",
                        dest="selection")

    parser.add_argument("--time-budget",
                        default=default_arguments["time budget"],
                        type=int,
                        help="the size of the time budget for the resulting test set (def=2500)",
                        dest="time_budget")

    arguments.pop(0)

    return parser.parse_args(arguments)


def validate_filename(filename):
    """ Validation of a input filename. Program exits in case of failure

    :param filename: seed file name
    :return: no return value
    """

    logger = logging.getLogger(default_arguments["logger"])

    if os.path.isfile(filename) == False:
        logger.critical("illegal seed file name or file doesn't exist")
        return status_code.ERR_FILE_NOT_FOUND

    return status_code.OK


def read_data(filename):
    """ Read data from seed file

    :param filename: seed file name
    :return: table data from seed file (table is represented as a list of rows, each row is a list of values)
    """

    # read excel file
    wb = xlrd.open_workbook(filename)

    for s in wb.sheets():
        # print 'Sheet:',s.name
        # actually there is break statement in the end of the first iteration of the cycle for sheets
        values = []
        for row in range(s.nrows):
            col_value = []
            for col in range(s.ncols):
                value = s.cell(row, col).value
                col_value.append(value)
            values.append(col_value)
        # break cycle after reading only first sheet
        break

    return values


def validate_data(arguments, values):
    """ Seed file data validation. Check that required columns exists, and that data in these columns has required data type

    :param arguments: parsed arguments
    :param values: read data from seed file (table with test cases)
    :return: no return value. Program exits in case of validation failure
    """

    logger = logging.getLogger(default_arguments["logger"])

    # check that <risk factor> column exists
    if arguments.risk_factor in values[0]:
        logger.info("Risk Factor column found: col %d, \"%s\"", values[0].index(arguments.risk_factor), arguments.risk_factor)
    else:
        logger.critical("Can't find Risk Factor column \"%s\" in seed file", arguments.risk_factor)
        return status_code.ERR_RISK_FACTOR_NOT_FOUND

    # check that <execution time> column exists
    if arguments.execution_time in values[0]:
        logger.info("Execution Time column found: col %d, \"%s\"", values[0].index(arguments.execution_time),
                    arguments.execution_time)
    else:
        logger.critical("Can't find Execution Time column \"%s\" in seed file", arguments.execution_time)
        return status_code.ERR_EXECUTION_TIME_NOT_FOUND

    # check that <selection> column exists
    if arguments.selection in values[0]:
        logger.info("Selection column found: col %d, \"%s\"", values[0].index(arguments.selection),
                    arguments.selection)
    else:
        logger.critical("Can't find Selection column \"%s\" in seed file", arguments.selection)
        return status_code.ERR_SELECTION_NOT_FOUND

    # check that <time budget> is a positive value
    if arguments.time_budget <= 0:
        logger.critical("Time budget is not a positive number: %d", arguments.time_budget)
        return status_code.ERR_TIME_BUDGET_NOT_POSITIVE

    # check that content of <risk factor> column can be converted to float, and convert
    rf = values[0].index(arguments.risk_factor)
    for i in range(1,len(values)):
        try:
            values[i][rf] = float(values[i][rf])
        except:
            logger.critical("Can't convert Risk Factor for test case # %d to float", i)
            return status_code.ERR_RISK_FACTOR_TYPE

    # check that content of <execution time> column can be converted to int, and convert
    et = values[0].index(arguments.execution_time)
    for i in range(1,len(values)):
        try:
            values[i][et] = int(values[i][et])
        except:
            logger.critical("Can't convert Execution Time for test case # %d to integer", i)
            return status_code.ERR_EXECUTION_TIME_TYPE

    if arguments.time_budget > MAX_BUDGET:
        logger.warning("Specified time budget is relatively big which may prevent from getting optimal solution")

    if len(values) >= MAX_TC:
        logger.warning("Number of test cases in seed file is relatively big which may prevent from getting optimal solution")

    return status_code.OK


def write_data(arguments, values):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Risk-based')

    for r in range(len(values)):
        for c in range(len(values[0])):
            ws.write(r, c, values[r][c])

    wb.save(arguments.filename)


def alg_dynamic_programming_01(arguments, values):
    """ Select test cases to build maximized risk coverage

    :param arguments: parsed arguments
    :param values: data from seed file
    :return: achieved risk ratio (achieved_risk_coverage/total_risk_value)
    """

    # number of test cases in <values>
    tc_count = len(values) - 1

    # index for execution_time column
    et = values[0].index(arguments.execution_time)

    # index for risk_factor column
    rf = values[0].index(arguments.risk_factor)

    # index for selection column
    sel = values[0].index(arguments.selection)

    # risk_mitigation[i][j] stores best risk coverage based on test cases 1..i with total execution time <=j
    risk_mitigation = [[0.0 for j in range(arguments.time_budget+1)] for i in range(0, tc_count+1)]

    # test_set[i][j] stores a test set associated with best risk coverage risk_mitigation[i][j]
    test_set = [[[] for j in range(arguments.time_budget+1)] for i in range(0, tc_count+1)]

    # solution for 0,1 knapsack problem using dynamic programming approach
    for i in range(1, tc_count+1):
        for j in range(0, arguments.time_budget+1):

            if values[i][et] > j:
                risk_mitigation[i][j] = risk_mitigation[i-1][j]
                # make sure that lists are copied, not referenced!
                test_set[i][j] = list(test_set[i-1][j])

            else:
                if risk_mitigation[i-1][j] > risk_mitigation[i-1][j-values[i][et]] + values[i][rf]:
                    risk_mitigation[i][j] = risk_mitigation[i - 1][j]
                    # make sure that lists are copied, not referenced!
                    test_set[i][j] = list(test_set[i - 1][j])
                else:
                    risk_mitigation[i][j] = risk_mitigation[i-1][j-values[i][et]] + values[i][rf]
                    test_set[i][j] = list(test_set[i-1][j-values[i][et]])
                    test_set[i][j].append(i)

    achieved_risk_coverage = 0.0
    total_risk_value = 0.0

    for i in range(1, tc_count+1):
        total_risk_value += values[i][rf]
        if i in test_set[tc_count][arguments.time_budget]:
            values[i][sel] = 1
            achieved_risk_coverage += values[i][rf]
        else:
            values[i][sel] = 0

    return achieved_risk_coverage/total_risk_value


if __name__ == "__main__":

    # init logging
    init_logger()
    logger = logging.getLogger(default_arguments["logger"])

    # parse input arguments
    arguments = parse_arguments(sys.argv)

    # validate seed file name
    ret = validate_filename(arguments.filename)
    if ret == status_code.ERR_FILE_NOT_FOUND:
        exit(ret)

    # read data from seed file
    try:
        data = read_data(arguments.filename)
    except Exception as e:
        logger.critical("Error reading seed file in XLRD")
        logger.debug("Exception: %s", e.message)
        exit(status_code.ERR_XLRD_READ)

    # validate data from seed file
    ret = validate_data(arguments, data)
    if ret != status_code.OK:
        exit(ret)

    # launching optimization algorithm to build test set
    try:
        logger.info("Building test coverage using dynamic programming algorithm for 01 knapsack problem with a time-budget of %d",
                    arguments.time_budget)
        a = alg_dynamic_programming_01(arguments, data)
        logger.info("Covered risk with porposed test set is %f", a)
        for i in range(0, len(data)):
            print(data[i])
    except MemoryError as e:
        logger.error("Caught MemoryError exception while building test set using dynamic programming algorithm for 01 knapsack problem")
        logger.info("Building test coverage using greedy approximation algorithm")

    # write_data(arguments, data)

    exit(status_code.OK)
