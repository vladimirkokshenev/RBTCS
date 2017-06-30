import unittest
import sys
sys.path.append('''C:\Git\RBTCS\package''')
import rbtcs

class TestParseArguments(unittest.TestCase):
    """Unit tests for class Arguments    """

    def test_default_values(self):
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'], rbtcs.default_arguments['filename']])
        self.assertEqual(args.filename, rbtcs.default_arguments['filename'])
        self.assertEqual(args.risk_factor, rbtcs.default_arguments['risk factor'])
        self.assertEqual(args.execution_time, rbtcs.default_arguments['execution time'])
        self.assertEqual(args.selection, rbtcs.default_arguments['selection'])
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])

    def test_filename(self):
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'], 'test.xls'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, rbtcs.default_arguments['risk factor'])
        self.assertEqual(args.execution_time, rbtcs.default_arguments['execution time'])
        self.assertEqual(args.selection, rbtcs.default_arguments['selection'])
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])

    def test_risk_factor(self):
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'], 'test.xls',
                                      '--risk-factor', 'risk factor col'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'risk factor col')
        self.assertEqual(args.execution_time, rbtcs.default_arguments['execution time'])
        self.assertEqual(args.selection, rbtcs.default_arguments['selection'])
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])

    def test_execution_time(self):
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test.xls',
                                      '--risk-factor', 'risk factor col',
                                      '--execution-time', 'execution time col'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'risk factor col')
        self.assertEqual(args.execution_time, 'execution time col')
        self.assertEqual(args.selection, rbtcs.default_arguments['selection'])
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])

    def test_selection(self):
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test.xls',
                                      '--risk-factor', 'risk factor col',
                                      '--execution-time', 'execution time col',
                                      '--selection', 'selected col'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'risk factor col')
        self.assertEqual(args.execution_time, 'execution time col')
        self.assertEqual(args.selection, 'selected col')
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])

    def test_time_budget(self):
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test.xls',
                                      '--risk-factor', 'risk factor col',
                                      '--execution-time', 'execution time col',
                                      '--selection', 'selected col',
                                      '--time-budget', '1000'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'risk factor col')
        self.assertEqual(args.execution_time, 'execution time col')
        self.assertEqual(args.selection, 'selected col')
        self.assertEqual(args.time_budget, 1000)

    def test_full_string(self):
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test.xls',
                                      '--risk-factor=rf',
                                      '--execution-time=et',
                                      '--selection=s',
                                      '--time-budget=1000'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'rf')
        self.assertEqual(args.execution_time, 'et')
        self.assertEqual(args.selection, 's')
        self.assertEqual(args.time_budget, 1000)

if __name__ == '__main__':
    unittest.main()