import unittest
import sys
import os
import logging
sys.path.append('''C:\Git\RBTCS\package''')
import rbtcs


class TestInitLogger(unittest.TestCase):
    """Fake unit test to trigger init_logger()"""

    def test_init_logger(self):
        """Just initializing logger"""
        rbtcs.init_logger()
        logging.disable(logging.CRITICAL)
        self.assertEquals(1, 1)


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
        if os.path.isfile('rbtcs_result.xls'):
            os.remove('rbtcs_result.xls')
        data2 = [[u'No', u'Risk Factor', u'Execution Time', u'Selected'], [1.0, 0.1, 10, u''], [2.0, 0.2, 20, u'']]
        rbtcs.write_data(arguments, data2)
        self.assertEquals(os.path.isfile('rbtcs_result.xls'), True)
        data = rbtcs.read_data('rbtcs_result.xls')
        self.assertEquals(data2, data)
        if os.path.isfile('rbtcs_result.xls'):
            os.remove('rbtcs_result.xls')


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


class TestOptimalAlgorithms(unittest.TestCase):
    """Unit tests for all implementations of algorithms with optimal solution"""

    def test_1(self):
        """seed data <test_alg_1.xlsx>, time budget 165"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_1.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=165'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_dynamic_programming_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [92.0, 23, 1], [57.0, 31, 1], [49.0, 29, 1],
             [68.0, 44, 1], [60.0, 53, 0], [43.0, 38, 1], [67.0, 63, 0], [84.0, 85, 0], [87.0, 89, 0], [72.0, 82, 0]]
        self.assertEquals(data, sol)

    def test_2(self):
        """seed data <test_alg_2.xlsx>, time budget 26"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_2.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=26'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_dynamic_programming_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [24.0, 12, 0], [13.0, 7, 1],
               [23.0, 11, 1], [15.0, 8, 1], [16.0, 9, 0]]
        self.assertEquals(data, sol)

    def test_3(self):
        """seed data <test_alg_3.xlsx>, time budget 190"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_3.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=190'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_dynamic_programming_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [50.0, 56, 1],
               [50.0, 59, 1], [64.0, 80, 0], [46.0, 64, 0], [50.0, 75, 1], [5.0, 17, 0]]
        self.assertEquals(data, sol)

    def test_4(self):
        """seed data <test_alg_4.xlsx>, time budget 50"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_4.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=50'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_dynamic_programming_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [70.0, 31, 1], [20.0, 10, 0],
               [39.0, 20, 0], [37.0, 19, 1], [7.0, 4, 0], [5.0, 3, 0], [10.0, 6, 0]]
        self.assertEquals(data, sol)

    def test_5(self):
        """seed data <test_alg_5.xlsx>, time budget 750"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_5.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=750'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_dynamic_programming_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [135.0, 70, 1], [139.0, 73, 0], [149.0, 77, 1],
               [150.0, 80, 0], [156.0, 82, 1], [163.0, 87, 0], [173.0, 90, 1], [184.0, 94, 1], [192.0, 98, 1],
               [201.0, 106, 0], [210.0, 110, 0], [214.0, 113, 0], [221.0, 115, 0], [229.0, 118, 1], [240.0, 120, 1]]
        self.assertEquals(data, sol)


    def test_6(self):
        """seed data <test_alg_6.xlsx>, time budget 6405"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_6.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=6405'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_dynamic_programming_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [825594.0, 382, 1], [1677009.0, 799, 1],
               [1676628.0, 909, 0], [1523970.0, 729, 1], [943972.0, 467, 1], [97426.0, 44, 1], [69666.0, 34, 0],
               [1296457.0, 698, 0], [1679693.0, 823, 0], [1902996.0, 903, 1], [1844992.0, 853, 1], [1049289.0, 551, 0],
               [1252836.0, 610, 1], [1319836.0, 670, 0], [953277.0, 488, 0], [2067538.0, 951, 1], [675367.0, 323, 0],
               [853655.0, 446, 0], [1826027.0, 931, 0], [65731.0, 31, 0], [901489.0, 496, 0], [577243.0, 264, 1],
               [466257.0, 224, 1], [369261.0, 169, 1]]
        self.assertEquals(data, sol)


class TestApproximateAlgorithms(unittest.TestCase):
    """Unit tests for all implementations of algorithms with approximate solution"""

    def test_1(self):
        """seed data <test_alg_1.xlsx>, time budget 165"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_1.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=165'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_greedy_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [92.0, 23, 1], [57.0, 31, 1], [49.0, 29, 1],
             [68.0, 44, 1], [60.0, 53, 0], [43.0, 38, 1], [67.0, 63, 0], [84.0, 85, 0], [87.0, 89, 0], [72.0, 82, 0]]
        self.assertEquals(data, sol)

    def test_2(self):
        """seed data <test_alg_2.xlsx>, time budget 26"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_2.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=26'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_greedy_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [24.0, 12, 1], [13.0, 7, 0],
               [23.0, 11, 1], [15.0, 8, 0], [16.0, 9, 0]]
        self.assertEquals(data, sol)

    def test_3(self):
        """seed data <test_alg_3.xlsx>, time budget 190"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_3.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=190'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_greedy_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [50.0, 56, 1],
               [50.0, 59, 1], [64.0, 80, 0], [46.0, 64, 1], [50.0, 75, 0], [5.0, 17, 0]]
        self.assertEquals(data, sol)

    def test_4(self):
        """seed data <test_alg_4.xlsx>, time budget 50"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_4.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=50'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_greedy_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [70.0, 31, 1], [20.0, 10, 1],
               [39.0, 20, 0], [37.0, 19, 0], [7.0, 4, 1], [5.0, 3, 1], [10.0, 6, 0]]
        self.assertEquals(data, sol)

    def test_5(self):
        """seed data <test_alg_5.xlsx>, time budget 750"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_5.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=750'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        rbtcs.alg_greedy_01(arguments, data)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [135.0, 70, 1], [139.0, 73, 1], [149.0, 77, 1],
               [150.0, 80, 0], [156.0, 82, 0], [163.0, 87, 0], [173.0, 90, 1], [184.0, 94, 1], [192.0, 98, 1],
               [201.0, 106, 0], [210.0, 110, 0], [214.0, 113, 0], [221.0, 115, 0], [229.0, 118, 1], [240.0, 120, 1]]
        self.assertEquals(data, sol)

    def test_6(self):
        """seed data <test300.xlsx>, time budget 750"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test300.xlsx',
                                           '--risk-factor', 'Risk Factor',
                                           '--execution-time', 'Execution Time',
                                           '--selection', 'Selected',
                                           '--time-budget=15000'])
        data = rbtcs.read_data(arguments.filename)
        rbtcs.validate_data(arguments, data)
        a = rbtcs.alg_greedy_01(arguments, data)
        self.assertEquals(a, 1.0)


class TestValidateFilename(unittest.TestCase):
    """Unit tests for validate_filename()"""

    def test_valide_filename_valid(self):
        """unit test for valid file name"""
        res = rbtcs.validate_filename('test_alg_1.xlsx')
        self.assertEquals(res, rbtcs.status_code.OK)

    def test_valide_filename_invalid(self):
        """unit test for invalid file name"""
        res = rbtcs.validate_filename('trash.trash')
        self.assertEquals(res, rbtcs.status_code.ERR_FILE_NOT_FOUND)

if __name__ == '__main__':
    unittest.main()
