import xlrd
import xlwt
import argparse
import sys
import os.path
import logging
import enum
from operator import itemgetter

default_arguments = {"rbtcs": "rbtcs.py",
                     "filename": "input.xlsx",
                     "risk factor": "Risk Factor",
                     "execution time": "Execution Time",
                     "selection": "Selected",
                     "time budget": 2500,
                     "prerequisites": "",
                     "logger": "rbtcs"}


class StatusCode(enum.Enum):
    OK = 1
    ERR_FILE_NOT_FOUND = 2
    ERR_XLRD_READ = 3
    ERR_RISK_FACTOR_NOT_FOUND = 4
    ERR_EXECUTION_TIME_NOT_FOUND = 5
    ERR_SELECTION_NOT_FOUND = 6
    ERR_TIME_BUDGET_NOT_POSITIVE = 7
    ERR_RISK_FACTOR_TYPE = 8
    ERR_EXECUTION_TIME_TYPE = 9
    ERR_HEADER_ROW_NOT_FOUND = 10
    ERR_HEADER_ROW_LAST = 11
    ERR_PREREQUISITES_TYPE = 12
    ERR_XLWT_WRITE = 13


MAX_BUDGET = 10000
MAX_ITEMS = 300


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
                        help="input file name (xls/xlsx)")

    parser.add_argument("-r",
                        default=default_arguments["risk factor"],
                        help="specify column name containing risk value associated with items (\"Risk Factor\" by default)",
                        dest="risk_factor")

    parser.add_argument("-t",
                        default=default_arguments["execution time"],
                        help="specify column name containing execution time associated with items (\"Execution Time\" by default)",
                        dest="execution_time")

    parser.add_argument("-s",
                        default=default_arguments["selection"],
                        help="specify column name to output coverage decisions (\"Selected\" by default)",
                        dest="selection")

    parser.add_argument("-b",
                        default=default_arguments["time budget"],
                        type=int,
                        help="specify the size of the time budget available for testing (2500 by default)",
                        dest="time_budget")

    parser.add_argument("-p",
                        default=default_arguments["prerequisites"],
                        help="specify column name with prerequisites associated with items (no prerequisites usage by default)",
                        dest="prerequisites")

    arguments.pop(0)

    return parser.parse_args(arguments)


def validate_filename(filename):
    """ Validation of a input filename. Program exits in case of failure

    :param filename: seed file name
    :return: no return value
    """

    logger = logging.getLogger(default_arguments["logger"])

    if os.path.isfile(filename) == False:
        logger.critical("%s is illegal input file name or file doesn't exist" % filename)
        return StatusCode.ERR_FILE_NOT_FOUND

    return StatusCode.OK


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


def detect_header_row(arguments, values):
    """
    Detection of a header row in an input file. The method searches for a row that contains risk-factor,
    execution-time and selection cells. All three should be in the same row. 
    
    :param arguments: command line arguments (including risk-factor, execution-time and selection)
    :param values: input file data (list of lists)
    :return: header row index
    """

    logger = logging.getLogger(default_arguments["logger"])

    cur_row = 0

    while cur_row < len(values):
        risk_factor_detected = arguments.risk_factor in values[cur_row]
        exec_time_detected = arguments.execution_time in values[cur_row]
        selection_detected = arguments.selection in values[cur_row]
        if arguments.prerequisites == "":
            prereq_detected = True
        else:
            prereq_detected = arguments.prerequisites in values[cur_row]

        # stop search if we found a row where all required headers are present
        if risk_factor_detected and exec_time_detected and selection_detected and prereq_detected:
            break
        cur_row += 1

    # if header row wasn't found (happens when cur_row == len(values))
    if cur_row == len(values):
        logger.critical("Header row not found!")
        exit(StatusCode.ERR_HEADER_ROW_NOT_FOUND)
    # if header row is the last row in the file - data is missing
    if cur_row == len(values)-1:
        logger.critical("Header row can't be the last row in the file!")
        exit(StatusCode.ERR_HEADER_ROW_LAST)
    # if header row was found - then log its number and return it
    if cur_row < len(values)-1:
        logger.debug("Header row index: %d", cur_row)
        logger.debug("Risk Factor column index: %d", values[cur_row].index(arguments.risk_factor))
        logger.debug("Execution Time column index: %d", values[cur_row].index(arguments.execution_time))
        logger.debug("Selection column index: %d", values[cur_row].index(arguments.selection))
        if arguments.prerequisites != "":
            logger.debug("Prerequisites column index: %d", values[cur_row].index(arguments.prerequisites))
        return cur_row


def validate_data(arguments, values, hdr_row):
    """ Seed file data validation. Check that required columns exists, and that data in these columns has required data type

    :param arguments: parsed arguments
    :param values: read data from seed file (table with test cases)
    :param hdr_row: header row index
    :return: no return value. Program exits in case of validation failure
    """

    logger = logging.getLogger(default_arguments["logger"])

    # check that <time budget> is a positive value
    if arguments.time_budget <= 0:
        logger.critical("Time budget is not a positive number: %d", arguments.time_budget)
        return StatusCode.ERR_TIME_BUDGET_NOT_POSITIVE

    # check that content of <risk factor> column can be converted to float, and convert
    rf = values[hdr_row].index(arguments.risk_factor)
    for i in range(hdr_row+1, len(values)):
        try:
            values[i][rf] = float(values[i][rf])
        except:
            # item i in values specifies item i+1 in excel (excel starts from 1)
            logger.critical("Can't convert Risk Factor for item in row # %d to float", i+1)
            return StatusCode.ERR_RISK_FACTOR_TYPE

    # check that content of <execution time> column can be converted to int, and convert
    et = values[hdr_row].index(arguments.execution_time)
    for i in range(hdr_row+1, len(values)):
        try:
            values[i][et] = int(values[i][et])
        except:
            # item i in values specifies item i+1 in excel (excel starts from 1)
            logger.critical("Can't convert Execution Time for item # %d to integer", i+1)
            return StatusCode.ERR_EXECUTION_TIME_TYPE

    # check that content of <prerequisites> column is a comma-separated list with integers
    if arguments.prerequisites != "":
        prereq = values[hdr_row].index(arguments.prerequisites)
        for i in range(hdr_row + 1, len(values)):
            if values[i][prereq] == "":
                values[i][prereq] = []
            else:
                prereq_list_converted = []
                # check if this is single-value cell (i.e. only one integer value provided as prerequisite)
                try:
                    single_prerequisite = int(float(values[i][prereq]))
                except:
                    # split comma-separated list of prerequisites into items
                    prereq_list = values[i][prereq].split(',')
                    for j in range(len(prereq_list)):
                        try:
                            single_prerequisite = int(prereq_list[j])
                        except:
                            # item i in values specifies item i+1 in excel (excel starts from 1)
                            logger.critical("Can't convert Prerequisites string for item # %d to list of integers ", i + 1)
                            return StatusCode.ERR_PREREQUISITES_TYPE
                        else:
                            prereq_list_converted.append(single_prerequisite)
                    values[i][prereq] = prereq_list_converted
                else:
                    prereq_list_converted.append(single_prerequisite)
                    values[i][prereq] = prereq_list_converted

    # check budget size
    if arguments.time_budget > MAX_BUDGET:
        logger.warning("Specified Time Budget is relatively big which may lead to sub-optimal solution")

    # check item count
    if len(values)-hdr_row-1 >= MAX_ITEMS:
        logger.warning("Number of Items in the input file is relatively big which may lead to sub-optimal solution")

    return StatusCode.OK


def prepare_data_for_writing(arguments, values, hdr_row):
    """ Current implementation convert prerequisites (that are stored as a list of integers) back into string.
    
    :param arguments: parsed arguments
    :param values: read data from seed file (table with test cases)
    :param hdr_row: header row index
    :return: no return value
    """

    prereq = values[hdr_row].index(arguments.prerequisites)
    for i in range(hdr_row + 1, len(values)):
        if values[i][prereq] == []:
            values[i][prereq] = ""
        else:
            prereq_str = ""
            for j in range(len(values[i][prereq])):
                if prereq_str == "":
                    prereq_str = prereq_str + str(values[i][prereq][j])
                else:
                    prereq_str = prereq_str + ',' + str(values[i][prereq][j])
            values[i][prereq] = prereq_str


def write_data(arguments, values):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('RBTCS')


    for r in range(len(values)):
        for c in range(len(values[0])):
            ws.write(r, c, values[r][c])

    wb.save('rbtcs_result.xls')


def alg_dynamic_programming_01(arguments, values, hdr_row):
    """ Select test cases to build maximized risk coverage using dynamic programming method for 01 knapsack

    :param arguments: parsed arguments
    :param values: data from seed file
    :param hdr_row: index of header row
    :return: achieved risk ratio (achieved_risk_coverage/total_risk_value)
    """

    # number of test cases in <values>
    tc_count = len(values) - hdr_row - 1

    # index for execution_time column
    et = values[hdr_row].index(arguments.execution_time)

    # index for risk_factor column
    rf = values[hdr_row].index(arguments.risk_factor)

    # index for selection column
    sel = values[hdr_row].index(arguments.selection)

    # test case #1 is in row (hdr_row+1)
    # test case #2 is in (hdr_row+2), etc.
    # risk_mitigation[i][j] stores best risk coverage based on test cases 1..i with total execution time <=j
    risk_mitigation = [[0.0 for j in range(arguments.time_budget+1)] for i in range(0, tc_count+1)]

    # test_set[i][j] stores a test set associated with best risk coverage risk_mitigation[i][j]
    test_set = [[[] for j in range(arguments.time_budget+1)] for i in range(0, tc_count+1)]

    # solution for 0,1 knapsack problem using dynamic programming approach
    for i in range(1, tc_count+1):
        for j in range(0, arguments.time_budget+1):

            if values[hdr_row+i][et] > j:
                risk_mitigation[i][j] = risk_mitigation[i-1][j]
                # make sure that lists are copied, not referenced!
                test_set[i][j] = list(test_set[i-1][j])

            else:
                if risk_mitigation[i-1][j] > risk_mitigation[i-1][j-values[hdr_row+i][et]] + values[hdr_row+i][rf]:
                    risk_mitigation[i][j] = risk_mitigation[i - 1][j]
                    # make sure that lists are copied, not referenced!
                    test_set[i][j] = list(test_set[i - 1][j])
                else:
                    risk_mitigation[i][j] = risk_mitigation[i-1][j-values[hdr_row+i][et]] + values[hdr_row+i][rf]
                    test_set[i][j] = list(test_set[i-1][j-values[hdr_row+i][et]])
                    test_set[i][j].append(i)

    achieved_risk_coverage = 0.0
    total_risk_value = 0.0

    for i in range(1, tc_count+1):
        total_risk_value += values[hdr_row+i][rf]
        if i in test_set[tc_count][arguments.time_budget]:
            values[hdr_row+i][sel] = 1
            achieved_risk_coverage += values[hdr_row+i][rf]
        else:
            values[hdr_row+i][sel] = 0

    return achieved_risk_coverage/total_risk_value


def alg_greedy_01(arguments, values, hdr_row):
    """ Select test cases to build maximized risk coverage using dynamic programming method for 01 knapsack

    :param arguments: parsed arguments
    :param values: data from seed file
    :param hdr_row: index of a header row
    :return: achieved risk ratio (achieved_risk_coverage/total_risk_value)
    """

    # number of test cases in <values>
    tc_count = len(values) - hdr_row - 1

    # index for execution_time column
    et = values[hdr_row].index(arguments.execution_time)

    # index for risk_factor column
    rf = values[hdr_row].index(arguments.risk_factor)

    # index for selection column
    sel = values[hdr_row].index(arguments.selection)

    # calculate risk density in separate list, we also store number of original test case
    risk_density = [[i, values[hdr_row+i][rf]/values[hdr_row+i][et]] for i in range(1, tc_count+1)]

    # sort seed data by rf/et values
    risk_density = sorted(risk_density, key=itemgetter(1), reverse=True)

    # use greedy strategy to put as many tc in a set as possible
    remaining_budget = arguments.time_budget

    for i in range(tc_count):
        if values[hdr_row+risk_density[i][0]][et] <= remaining_budget:
            values[hdr_row+risk_density[i][0]][sel] = 1
            remaining_budget -= values[hdr_row+risk_density[i][0]][et]
        else:
            values[hdr_row+risk_density[i][0]][sel] = 0

    # calculate achieved_risk_ration = achieved_risk_coverage/total_risk_value
    achieved_risk_coverage = 0.0
    total_risk_value = 0.0

    for i in range(1, tc_count + 1):
        total_risk_value += values[hdr_row+i][rf]
        if values[hdr_row+i][sel] == 1:
            achieved_risk_coverage += values[hdr_row+i][rf]

    return achieved_risk_coverage / total_risk_value


if __name__ == "__main__":

    # init logging
    init_logger()
    logger = logging.getLogger(default_arguments["logger"])

    # parse input arguments
    arguments = parse_arguments(sys.argv)

    # validate seed file name
    ret = validate_filename(arguments.filename)
    if ret == StatusCode.ERR_FILE_NOT_FOUND:
        exit(ret)

    # read data from seed file
    try:
        data = read_data(arguments.filename)
    except Exception as e:
        logger.critical("Error reading input file in XLRD")
        logger.debug("XLRD Exception: %s", e.message)
        exit(StatusCode.ERR_XLRD_READ)

    # validate data from seed file
    hdr_row = detect_header_row(arguments, data)
    ret = validate_data(arguments, data, hdr_row)
    if ret != StatusCode.OK:
        exit(ret)

    # launching optimization algorithm to build test set
    if arguments.prerequisites == "":
        try:
            logger.info("Building test coverage using optimal algorithm")
            a = alg_dynamic_programming_01(arguments, data, hdr_row)
            logger.info("Covered risk with proposed test set using optimal algorithms is %f", a)
        except MemoryError as e:
            logger.error("Caught MemoryError exception while building test set using dynamic programming algorithm for 01 knapsack problem")
            logger.info("Building test coverage using greedy approximation algorithm")
            a = alg_greedy_01(arguments, data, hdr_row)
            logger.info("Covered risk with proposed test set using greedy method is %f", a)
    else:
        logger.info("Building test coverage using greedy approximation algorithm with prerequisites support")

    prepare_data_for_writing(arguments, data, hdr_row)

    try:
        write_data(arguments, data)
    except Exception as e:
        logger.critical("Error writing results file in XLWT")
        logger.debug("XLWT Exception: %s", e.message)
        exit(StatusCode.ERR_XLWT_WRITE)

    exit(StatusCode.OK)
