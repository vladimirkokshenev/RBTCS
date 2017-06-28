import unittest
import sys
sys.path.append('''C:\Git\RBTCS\package''')
import rbtcs

class TestArgumentsConstruction(unittest.TestCase):
    """Unit tests for class Arguments    """

    def test_default_values(self):
        args = rbtcs.Arguments()
        self.assertEqual(args.filename, 'testcases.xls')
        self.assertEqual(args.risk_factor_col, 'Risk Factor')
        self.assertEqual(args.execution_time_col, 'Execution Time')
        self.assertEqual(args.selection_col, 'Selected')
        self.assertEqual(args.time_budget, 2500)

    def test_nondefault_values(self):
        filename = "test.xls"
        risk_factor_col = "Risk Factor Test"
        execution_time_col = "Execution Time Test"
        selection_col = "Selected Test"
        time_budget = 100500
        args = rbtcs.Arguments(filename, risk_factor_col, execution_time_col, selection_col, time_budget)
        self.assertEqual(args.filename, filename)
        self.assertEqual(args.risk_factor_col, risk_factor_col)
        self.assertEqual(args.execution_time_col, execution_time_col)
        self.assertEqual(args.selection_col, selection_col)
        self.assertEqual(args.time_budget, time_budget)


if __name__ == '__main__':
    unittest.main()