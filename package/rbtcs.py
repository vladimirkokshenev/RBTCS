import xlrd
import xlwt
import argparse
import sys
import os.path

default_arguments = {"rbtcs": "rbtcs.py",
                     "filename": "testcases.xls",
                     "risk factor": "Risk Factor",
                     "execution time": "Execution Time",
                     "selection": "Selected",
                     "time budget": 2500}


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

    if os.path.isfile(filename) == False:
        print("ERROR: illegal file name or file doesn't exist")
        sys.exit(0)


def read_data(filename):
    """

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
                value = (s.cell(row, col).value)
                # following try/catch will convert float values to float, but integer values will stay as strings
                try:
                    value = str(int(value))
                except:
                    pass
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

    # check that <risk factor> column exists
    if arguments.risk_factor in values[0]:
        print("Risk Factor column found: col %d, \"%s\"" % (values[0].index(arguments.risk_factor),
                                                            arguments.risk_factor))
    else:
        print("ERROR: Can't find Risk Factor column \"%s\" in seed file" % arguments.risk_factor)
        sys.exit(0)

    # check that <execution time> column exists
    if arguments.execution_time in values[0]:
        print("Execution Time column found: col %d, \"%s\"" % (values[0].index(arguments.execution_time),
                                                               arguments.execution_time))
    else:
        print("ERROR: Can't find Execution Time column \"%s\" in seed file" % arguments.execution_time)
        sys.exit(0)

    # check that <selection> column exists
    if arguments.selection in values[0]:
        print("Selection column found: %d, \"%s\"" % (values[0].index(arguments.selection),
                                                      arguments.selection))
    else:
        print("ERROR: Can't find Selection column \"%s\" in seed file" % arguments.selection)
        sys.exit(0)

    # check that content of <risk factor> column can be converted to float, and convert
    rf = values[0].index(arguments.risk_factor)
    for i in range(1,len(values)):
        try:
            values[i][rf] = float(values[i][rf])
        except:
            print("ERROR: Can't convert value %d in risk factor column \"%s\" into float" % (i,arguments.risk_factor))
            sys.exit(0)

    # check that content of <execution time> column can be converted to int, and convert
    et = values[0].index(arguments.execution_time)
    for i in range(1,len(values)):
        try:
            values[i][et] = int(values[i][et])
        except:
            print("ERROR: Can't convert value %d in execution time column \"%s\" into integer" % (i, arguments.execution_time))
            sys.exit(0)


def write_data(arguments, values):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Risk-based')

    for r in range(len(values)):
        for c in range(len(values[0])):
            ws.write(r, c, values[r][c])

    wb.save("example.xls")


if __name__ == "__main__":

    arguments = parse_arguments(sys.argv)
    validate_filename(arguments.filename)
    data = read_data(arguments.filename)
    validate_data(arguments, data)
    write_data(arguments,data)
    # print(data)
