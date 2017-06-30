from xlrd import open_workbook
import argparse
import sys

default_arguments = {"filename": "testcases.xls",
                     "risk factor": "Risk Factor",
                     "execution time": "Execution Time",
                     "selection": "Selected",
                     "time budget": 2500,
                     "rbtcs": "rbtcs.py"}

def parse_arguments(arguments):
    """Parse input arguments for RBTCS tool.

    Arguments:
        argument -- string that contain input arguments
    Return Value:
        result of parser.parse_args() method
    """

    parser = argparse.ArgumentParser(description="Risk-Based Test Case Selector Tool")

    parser.add_argument("filename",
                        default=default_arguments["filename"],
                        help="the seed file with test cases")

    parser.add_argument("--risk-factor",
                        default=default_arguments["risk factor"],
                        help="the column name containing risk factor of a test case",
                        dest="risk_factor")

    parser.add_argument("--execution-time",
                        default=default_arguments["execution time"],
                        help="the column name containing execution time of a test case",
                        dest="execution_time")

    parser.add_argument("--selection",
                        default=default_arguments["selection"],
                        help="the column name with a test case selection into resulting test set",
                        dest="selection")

    parser.add_argument("--time-budget",
                        default=default_arguments["time budget"],
                        type=int,
                        help="the size of the time budget for the resulting test set",
                        dest="time_budget")

    arguments.pop(0)

    return parser.parse_args(arguments)

def read_seed_file(filename="testcases.xls"):
    """Read seed file, and do input validation for columns risk-factor and execution_time"""
    return 0

def build_test_set():
    """Build a set of test cases according to requested optimization"""
    return 0


if __name__ == "__main__":
    print(sys.argv)
    a = parse_arguments(sys.argv)
    print(a)
