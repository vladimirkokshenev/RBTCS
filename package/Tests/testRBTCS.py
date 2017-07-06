import unittest
import sys
import os
sys.path.append('''C:\Git\RBTCS\package''')
import rbtcs


class TestParseArguments(unittest.TestCase):
    """Unit tests for parse_arguments()    """

    def test_default_values(self):
        """ Testing parse_arguments() with default values for filename,
        risk-factor, execution-time, selection and time-budget. """
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'], rbtcs.default_arguments['filename']])
        self.assertEqual(args.filename, rbtcs.default_arguments['filename'])
        self.assertEqual(args.risk_factor, rbtcs.default_arguments['risk factor'])
        self.assertEqual(args.execution_time, rbtcs.default_arguments['execution time'])
        self.assertEqual(args.selection, rbtcs.default_arguments['selection'])
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])

    def test_filename(self):
        """ Testing parse_arguments() with non-default value for filename. """
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'], 'test.xls'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, rbtcs.default_arguments['risk factor'])
        self.assertEqual(args.execution_time, rbtcs.default_arguments['execution time'])
        self.assertEqual(args.selection, rbtcs.default_arguments['selection'])
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])

    def test_risk_factor(self):
        """ Testing parse_arguments() with non-default values for filename, risk-factor """
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'], 'test.xls',
                                      '--risk-factor', 'risk factor col'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'risk factor col')
        self.assertEqual(args.execution_time, rbtcs.default_arguments['execution time'])
        self.assertEqual(args.selection, rbtcs.default_arguments['selection'])
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])

    def test_execution_time(self):
        """ Testing parse_arguments() with non-default values for filename, risk-factor, execution-time """

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
        """ Testing parse_arguments() with non-default values for filename, risk-factor, execution-time, selection """

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
        """ Testing parse_arguments() with non-default values for filename, risk-factor, execution-time, selection, time-budget """

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
        """ Testing parse_arguments() with non-default values using '=' sign for filename, risk-factor, execution-time, selection """

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


class TestReadWriteData(unittest.TestCase):
    """Unit tests for read_data()    """

    def test_read_data(self):
        """ Check read_data() with simple seed file 'test_read_data_1.xlsx' """
        data = rbtcs.read_data('test_read_data_1.xlsx')
        data2 = [[u'No', u'Risk Factor', u'Execution Time', u'Selected'], [1.0, 0.1, 10.0, u''], [2.0, 0.2, 20.0, u'']]
        self.assertEqual(data, data2)

    def test_write_data(self):
        """ Test write_data() with simple seed data.
        Firstly, make sure that file doesn't exist (if so - delete it).
        Then write a file from simple seed data and make sure file appeard"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_write_data_1.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=1000'])
        if os.path.isfile(arguments.filename):
            os.remove(arguments.filename)
        data2 = [[u'No', u'Risk Factor', u'Execution Time', u'Selected'], [1.0, 0.1, 10, u''], [2.0, 0.2, 20, u'']]
        rbtcs.write_data(arguments, data2)
        self.assertEquals(os.path.isfile(arguments.filename), True)
        data = rbtcs.read_data(arguments.filename)
        self.assertEquals(data2, data)
        if os.path.isfile(arguments.filename):
            os.remove(arguments.filename)


class TestValidateData(unittest.TestCase):
    """Unit tests for validate_data()    """

    def test_validate_data_1(self):
        """ Unit test for basic data validation with test seed file 'test_read_data_1.xlsx'.
        Test seed file contains columns 'Risk Factor', 'Execution Time', 'Selected'.
        'Risk Factor column contains float data and should keep float.
        'Execution Time' column contains integer data and should stay integer"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test_read_data_1.xlsx',
                                      '--risk-factor', 'Risk Factor',
                                      '--execution-time', 'Execution Time',
                                      '--selection', 'Selected',
                                      '--time-budget=1000'])
        data = rbtcs.read_data(arguments.filename)
        ret = rbtcs.validate_data(arguments, data)
        self.assertEquals(ret, rbtcs.status_code.OK)
        data2 = [[u'No', u'Risk Factor', u'Execution Time', u'Selected'], [1.0, 0.1, 10, u''], [2.0, 0.2, 20, u'']]
        self.assertEqual(data, data2)

    def test_validate_data_2(self):
        """ Unit test for basic data validation with test seed file 'test_read_data_2.xlsx'.
        Test seed file contains columns 'Risk Factor', 'Execution Time', 'Selected'.
        'Risk Factor' column contains integer data and should be converted to float.
        'Execution Time' column contains float data and should be converted to integer"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test_read_data_2.xlsx',
                                      '--risk-factor', 'Risk Factor',
                                      '--execution-time', 'Execution Time',
                                      '--selection', 'Selected',
                                      '--time-budget=1000'])
        data = rbtcs.read_data(arguments.filename)
        ret = rbtcs.validate_data(arguments, data)
        self.assertEquals(ret, rbtcs.status_code.OK)
        data2 = [[u'No', u'Risk Factor', u'Execution Time', u'Selected'], [1.0, 1.0, 10, u''], [2.0, 2.0, 20, u'']]
        self.assertEqual(data, data2)

    def test_validate_data_wrong_risk_factor(self):
        """ Unit test for data validation in case of missing Risk Factor column"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_read_data_1.xlsx',
                                           '--risk-factor', 'Risk F',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=1000'])
        data = rbtcs.read_data(arguments.filename)
        ret = rbtcs.validate_data(arguments, data)
        self.assertEquals(ret, rbtcs.status_code.ERR_RISK_FACTOR_NOT_FOUND)

    def test_validate_data_wrong_execution_time(self):
        """ Unit test for data validation in case of missing Execution Time column"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_read_data_1.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution T',
                                           '--selection', 'Selected',
                                           '--time-budget=1000'])
        data = rbtcs.read_data(arguments.filename)
        ret = rbtcs.validate_data(arguments, data)
        self.assertEquals(ret, rbtcs.status_code.ERR_EXECUTION_TIME_NOT_FOUND)

    def test_validate_data_wrong_selection(self):
        """ Unit test for data validation in case of missing Selection column"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_read_data_1.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Sel',
                                           '--time-budget=1000'])
        data = rbtcs.read_data(arguments.filename)
        ret = rbtcs.validate_data(arguments, data)
        self.assertEquals(ret, rbtcs.status_code.ERR_SELECTION_NOT_FOUND)

    def test_validate_data_negative_time_budget(self):
        """ Unit test for data validation in case of negative Time Budget"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_read_data_1.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=-1'])
        data = rbtcs.read_data(arguments.filename)
        ret = rbtcs.validate_data(arguments, data)
        self.assertEquals(ret, rbtcs.status_code.ERR_TIME_BUDGET_NOT_POSITIVE)

    def test_validate_data_risk_factor_non_float(self):
        """ Unit test for data validation in case of Risk Factor value non-convertable to float"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_risk_factor.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=1000'])
        data = rbtcs.read_data(arguments.filename)
        ret = rbtcs.validate_data(arguments, data)
        self.assertEquals(ret, rbtcs.status_code.ERR_RISK_FACTOR_TYPE)

    def test_validate_data_execution_time_non_integer(self):
        """ Unit test for data validation in case of Execution Time value non-convertable to int"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_execution_time.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=1000'])
        data = rbtcs.read_data(arguments.filename)
        ret = rbtcs.validate_data(arguments, data)
        self.assertEquals(ret, rbtcs.status_code.ERR_EXECUTION_TIME_TYPE)

if __name__ == '__main__':
    unittest.main()