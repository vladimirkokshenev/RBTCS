from xlrd import open_workbook

class Arguments:
    """Class to store input arguments for RBTCS tool"""

    def __init__(self,
                 filename="testcases.xls",
                 risk_factor_col="Risk Factor",
                 execution_time_col="Execution Time",
                 selection_col="Selected",
                 time_budget=2500):
        """Init"""
        self.filename = filename
        self.risk_factor_col = risk_factor_col
        self.execution_time_col = execution_time_col
        self.selection_col = selection_col
        self.time_budget = time_budget


def parse_args(args=None):
    """Parse input arguments for RBTCS tool.

    Arguments:
        args -- string that contain call arguments
    Return Value:
        instance of class Arguments with parameters set according input args
    """
    print(args)
    return Arguments()

def read_seed_file(filename="testcases.xls"):
    """Read seed file, and do input validation for columns risk-factor and execution_time"""
    return 0

def build_test_set():
    """Build a set of test cases according to requested optimization"""
    return 0


if __name__ == '__main__':
    args = parse_args()
    print(args.filename,args.risk_factor_col,args.execution_time_col,args.selection_col,args.time_budget)
