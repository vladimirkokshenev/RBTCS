import unittest
import sys
sys.path.append('''C:\Git\RBTCS\package''')
import rbtcs
import os
import logging

class TestInitLogger(unittest.TestCase):
    """Fake unit test to trigger init_logger()"""

    def test_init_logger(self):
        """Just initializing logger"""
        rbtcs.init_logger()
        logging.disable(logging.CRITICAL)
        self.assertEquals(1, 1)


# parse_arguments()
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
        self.assertEqual(args.prerequisites, rbtcs.default_arguments['prerequisites'])

    def test_filename(self):
        """ Testing parse_arguments() with non-default value for filename. """
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'], 'test.xls'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, rbtcs.default_arguments['risk factor'])
        self.assertEqual(args.execution_time, rbtcs.default_arguments['execution time'])
        self.assertEqual(args.selection, rbtcs.default_arguments['selection'])
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])
        self.assertEqual(args.prerequisites, rbtcs.default_arguments['prerequisites'])

    def test_risk_factor(self):
        """ Testing parse_arguments() with non-default values for filename, risk-factor """
        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'], 'test.xls',
                                      '-r', 'risk factor col'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'risk factor col')
        self.assertEqual(args.execution_time, rbtcs.default_arguments['execution time'])
        self.assertEqual(args.selection, rbtcs.default_arguments['selection'])
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])
        self.assertEqual(args.prerequisites, rbtcs.default_arguments['prerequisites'])

    def test_execution_time(self):
        """ Testing parse_arguments() with non-default values for filename, risk-factor, execution-time """

        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test.xls',
                                      '-r', 'risk factor col',
                                      '-t', 'execution time col'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'risk factor col')
        self.assertEqual(args.execution_time, 'execution time col')
        self.assertEqual(args.selection, rbtcs.default_arguments['selection'])
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])

    def test_selection(self):
        """ Testing parse_arguments() with non-default values for filename, risk-factor, execution-time, selection """

        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test.xls',
                                      '-r', 'risk factor col',
                                      '-t', 'execution time col',
                                      '-s', 'selected col'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'risk factor col')
        self.assertEqual(args.execution_time, 'execution time col')
        self.assertEqual(args.selection, 'selected col')
        self.assertEqual(args.time_budget, rbtcs.default_arguments['time budget'])

    def test_time_budget(self):
        """ Testing parse_arguments() with non-default values for filename, risk-factor, execution-time, selection, time-budget """

        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test.xls',
                                      '-r', 'risk factor col',
                                      '-t', 'execution time col',
                                      '-s', 'selected col',
                                      '-b', '1000'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'risk factor col')
        self.assertEqual(args.execution_time, 'execution time col')
        self.assertEqual(args.selection, 'selected col')
        self.assertEqual(args.time_budget, 1000)

    def test_prerequisites(self):
        """ Testing parse_arguments() with non-default values for filename, risk-factor, execution-time, selection, 
        time-budget, and prerequisites
        """

        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                        'test.xls',
                                        '-r', 'risk factor col',
                                        '-t', 'execution time col',
                                        '-s', 'selected col',
                                        '-b', '1000',
                                        '-p', 'prerequisites col'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'risk factor col')
        self.assertEqual(args.execution_time, 'execution time col')
        self.assertEqual(args.selection, 'selected col')
        self.assertEqual(args.time_budget, 1000)
        self.assertEqual(args.prerequisites, 'prerequisites col')

    def test_full_string(self):
        """ Testing parse_arguments() with non-default values using '=' sign for filename, risk-factor, execution-time, selection """

        args = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test.xls',
                                      '-r=rf',
                                      '-t=et',
                                      '-s=s',
                                      '-b=1000',
                                      '-p=p'])
        self.assertEqual(args.filename, 'test.xls')
        self.assertEqual(args.risk_factor, 'rf')
        self.assertEqual(args.execution_time, 'et')
        self.assertEqual(args.selection, 's')
        self.assertEqual(args.time_budget, 1000)
        self.assertEqual(args.prerequisites, 'p')


# read_data()
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
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b', '1000'])
        if os.path.isfile('rbtcs_result.xls'):
            os.remove('rbtcs_result.xls')
        data2 = [[u'No', u'Risk Factor', u'Execution Time', u'Selected'], [1.0, 0.1, 10, u''], [2.0, 0.2, 20, u'']]
        rbtcs.write_data(arguments, data2)
        self.assertEquals(os.path.isfile('rbtcs_result.xls'), True)
        data = rbtcs.read_data('rbtcs_result.xls')
        self.assertEquals(data2, data)
        if os.path.isfile('rbtcs_result.xls'):
            os.remove('rbtcs_result.xls')


# detect_header_row()
class TestDetectHeaderRow(unittest.TestCase):
    """Unit tests for detect_header_row().
    For now (due to current code structure) we can't properly test in unit tests two cases: 
      1. when header row wasn't detected;
      2. when header row is the last row
    """

    def test_detect_header_row_0(self):
        """Test when header row is row # 0"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_header_row_1.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=1000'])
        data = rbtcs.read_data(arguments.filename)
        res = rbtcs.detect_header_row(arguments, data)
        self.assertEqual(res, 0)

    def test_detect_header_row_1(self):
        """Test when header row is row # 1"""

        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_header_row_2.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=1000'])
        data = rbtcs.read_data(arguments.filename)
        res = rbtcs.detect_header_row(arguments, data)
        self.assertEqual(res, 1)

    def test_detect_header_row_2(self):
        """Test when header row is row # 17 (using risk-based worksheet as data source)"""

        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_header_row_3.xlsx',
                                           '-r', 'Risk Value',
                                           '-t', 'Execution Cost',
                                           '-s', 'Removed (y)?',
                                           '-b=1000'])
        data = rbtcs.read_data(arguments.filename)
        res = rbtcs.detect_header_row(arguments, data)
        self.assertEqual(res, 17)

    def test_detect_header_row_3(self):
        """Test when header row is row # 17 (using risk-based worksheet as data source + prerequisites column)"""

        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_header_row_4.xlsx',
                                           '-r', 'Risk Value',
                                           '-t', 'Execution Cost',
                                           '-s', 'Removed (y)?',
                                           '-b=1000',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        res = rbtcs.detect_header_row(arguments, data)
        self.assertEqual(res, 17)


# validate_data()
class TestValidateData(unittest.TestCase):
    """Unit tests for validate_data()    """

    def test_validate_data_1(self):
        """ Unit test for basic data validation with test seed file 'test_read_data_1.xlsx'.
        Test seed file contains columns 'Risk Factor', 'Execution Time', 'Selected'.
        'Risk Factor column contains float data and should keep float.
        'Execution Time' column contains integer data and should stay integer"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test_read_data_1.xlsx',
                                      '-r', 'Risk Factor',
                                      '-t', 'Execution Time',
                                      '-s', 'Selected',
                                      '-b=1000'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEquals(ret, rbtcs.StatusCode.OK)
        data2 = [[u'No', u'Risk Factor', u'Execution Time', u'Selected'], [1.0, 0.1, 10, u''], [2.0, 0.2, 20, u'']]
        self.assertEqual(data, data2)

    def test_validate_data_2(self):
        """ Unit test for basic data validation with test seed file 'test_read_data_2.xlsx'.
        Test seed file contains columns 'Risk Factor', 'Execution Time', 'Selected'.
        'Risk Factor' column contains integer data and should be converted to float.
        'Execution Time' column contains float data and should be converted to integer"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                      'test_read_data_2.xlsx',
                                      '-r', 'Risk Factor',
                                      '-t', 'Execution Time',
                                      '-s', 'Selected',
                                      '-b=1000'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEquals(ret, rbtcs.StatusCode.OK)
        data2 = [[u'No', u'Risk Factor', u'Execution Time', u'Selected'], [1.0, 1.0, 10, u''], [2.0, 2.0, 20, u'']]
        self.assertEqual(data, data2)


    def test_validate_data_negative_time_budget(self):
        """ Unit test for data validation in case of negative Time Budget"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_read_data_1.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=-1'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEquals(ret, rbtcs.StatusCode.ERR_TIME_BUDGET_NOT_POSITIVE)

    def test_validate_data_risk_factor_non_float(self):
        """ Unit test for data validation in case of Risk Factor value non-convertable to float"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_risk_factor.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=1000'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEquals(ret, rbtcs.StatusCode.ERR_RISK_FACTOR_TYPE)

    def test_validate_data_execution_time_non_integer(self):
        """ Unit test for data validation in case of Execution Time value non-convertable to int"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_execution_time.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=1000'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEquals(ret, rbtcs.StatusCode.ERR_EXECUTION_TIME_TYPE)

    def test_validate_data_prerequisites_ok(self):
        """ Unit test for validate_data() when prerquisites correct"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_prerequisites.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEqual(ret, rbtcs.StatusCode.OK)
        prereqind = data[hdr_row].index(arguments.prerequisites)
        self.assertEqual(data[hdr_row+2][prereqind], [1])
        self.assertEqual(data[hdr_row + 3][prereqind], [])
        self.assertEqual(data[hdr_row + 4][prereqind], [1, 2])
        self.assertEqual(data[hdr_row + 10][prereqind], [1, 2, 3, 4, 5, 6])

    def test_validate_data_prerequisites_err(self):
        """ Unit test for validate_data() when prerquisites incorrect"""

        # first check to verify that single non-int value caught ('a' in cell)
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_prerequisites_err1.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEqual(ret, rbtcs.StatusCode.ERR_PREREQUISITES_TYPE)

        # second check to verify that list with non-int value caught ('1,2,ba' in cell)
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_prerequisites_err2.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEqual(ret, rbtcs.StatusCode.ERR_PREREQUISITES_TYPE)

        # 3rd, 4th, and 5th checks to verify that list with values below 1 or above max FRID numbers
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_prerequisites_err3.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEqual(ret, rbtcs.StatusCode.ERR_PREREQUISITES_TYPE)

        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_prerequisites_err4.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEqual(ret, rbtcs.StatusCode.ERR_PREREQUISITES_TYPE)

        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_prerequisites_err5.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEqual(ret, rbtcs.StatusCode.ERR_PREREQUISITES_TYPE)


# extract_items()
class TestExtractItems(unittest.TestCase):
    """Unit tests for extract_items()    """
    def test_extract_items_with_prerequisites(self):
        """ Unit test for extract_items() with prerequisites (single precondition, list of preconditions, list with duplicates """
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_prerequisites.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        self.assertEqual(items[0], {"ID": 0, "RF": 2.0, "ET": 2, "SL": rbtcs.ITEM_SELECTED_BY_USER, "PR": []})
        self.assertEqual(items[1], {"ID": 1, "RF": 8.0, "ET": 3, "SL": rbtcs.ITEM_EXCLUDED_BY_USER, "PR": [1]})
        self.assertEqual(items[8], {"ID": 8, "RF": 17.333333333333332, "ET": 4, "SL": rbtcs.ITEM_SELECTED_BY_USER, "PR": [1, 2, 3]})
        self.assertEqual(items[9], {"ID": 9, "RF": 19.833333333333332, "ET": 1, "SL": rbtcs.ITEM_NOT_SELECTED_BY_ALG, "PR": [1, 2, 3, 4, 5, 6]})

    def test_extract_items_with_no_prerequisites(self):
        """ Unit test for extract_items() without prerequisites """
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_1.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=1000'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        self.assertEqual(items[0], {"ID": 0, "RF": 92.0, "ET": 23, "SL": rbtcs.ITEM_NOT_SELECTED_BY_ALG})
        self.assertEqual(items[9], {"ID": 9, "RF": 72.0, "ET": 82, "SL": rbtcs.ITEM_NOT_SELECTED_BY_ALG})

    def test_extract_items_with_seed(self):
        """ Unit test for extract_items() with seed data """
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_extract_items_seed.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        self.assertEqual(items[0], {"ID": 0, "RF": 2.0, "ET": 2, "SL": rbtcs.ITEM_NOT_SELECTED_BY_ALG})
        self.assertEqual(items[2], {"ID": 2, "RF": 18.0, "ET": 4, "SL": rbtcs.ITEM_SELECTED_BY_USER})
        self.assertEqual(items[6], {"ID": 6, "RF": 9.0, "ET": 10, "SL": rbtcs.ITEM_EXCLUDED_BY_USER})


# handle_seeding_data(items, arguments, hdr_row)
class TestHandleSeedingData(unittest.TestCase):

    def test_handle_seeding_data_contradiction_precondition(self):
        """ Test that contradiction between positive seeding and negative seeding is detected"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_seeding_contradiction_precondition.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000',
                                           '-p', 'Preconditions'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        err_status = rbtcs.handle_seeding_data(items, arguments, hdr_row)
        self.assertEqual(err_status, rbtcs.StatusCode.ERR_SEEDING_CONTRADICTION)

    def test_handle_seeding_data_contradiction_oversubscription(self):
        """ Test that budget oversubscription by positive seeding is detected"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_seeding_contradiction_oversubscription.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=20',
                                           '-p', 'Preconditions'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        err_status = rbtcs.handle_seeding_data(items, arguments, hdr_row)
        self.assertEqual(err_status, rbtcs.StatusCode.ERR_SEEDING_CONTRADICTION)

    def test_handle_seeding_data_contradiction_oversubscription_2(self):
        """ Test that budget oversubscription by positive seeding is detected"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_seeding_contradiction_oversubscription2.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=13',
                                           '-p', 'Preconditions'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        err_status = rbtcs.handle_seeding_data(items, arguments, hdr_row)
        self.assertEqual(err_status, rbtcs.StatusCode.ERR_SEEDING_CONTRADICTION)

    def test_handle_seeding_data_negative_seeding(self):
        """ Test that negative seeding is handled correctly"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_negative_seeding.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=100',
                                           '-p', 'Preconditions'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        err_status = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEqual(err_status, rbtcs.StatusCode.OK)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        err_status = rbtcs.handle_seeding_data(items, arguments, hdr_row)
        self.assertEqual(err_status, rbtcs.StatusCode.OK)
        self.assertEqual(items[0], {"ID": 0, "RF": 2.0, "ET": 2, "SL": rbtcs.ITEM_NOT_SELECTED_BY_ALG, "PR": []})
        self.assertEqual(items[1], {"ID": 1, "RF": 8.0, "ET": 4, "SL": rbtcs.ITEM_EXCLUDED_BY_USER, "PR": [1, 10]})
        self.assertEqual(items[2]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[3]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[4]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[5]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[6]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[7]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[8]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[9], {"ID": 9, "RF": 22.50, "ET": 7, "SL": rbtcs.ITEM_EXCLUDED_BY_USER, "PR": [11]})
        self.assertEqual(items[10], {"ID": 10, "RF": 0.0, "ET": 10, "SL": rbtcs.ITEM_EXCLUDED_BY_USER, "PR": []})

    def test_handle_seeding_data_positive_seeding(self):
        """ Test that negative seeding is handled correctly"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_positive_seeding.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=100',
                                           '-p', 'Preconditions'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        err_status = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEqual(err_status, rbtcs.StatusCode.OK)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        err_status = rbtcs.handle_seeding_data(items, arguments, hdr_row)
        self.assertEqual(err_status, rbtcs.StatusCode.OK)
        self.assertEqual(items[0], {"ID": 0, "RF": 2.0, "ET": 2, "SL": rbtcs.ITEM_SELECTED_BY_USER, "PR": []})
        self.assertEqual(items[1], {"ID": 1, "RF": 8.0, "ET": 4, "SL": rbtcs.ITEM_NOT_SELECTED_BY_ALG, "PR": []})
        self.assertEqual(items[2]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[3]["SL"], rbtcs.ITEM_SELECTED_BY_USER)
        self.assertEqual(items[4]["SL"], rbtcs.ITEM_SELECTED_BY_USER)
        self.assertEqual(items[5]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[6]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[7]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[8]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[9], {"ID": 9, "RF": 22.50, "ET": 7, "SL": rbtcs.ITEM_SELECTED_BY_USER, "PR": []})
        self.assertEqual(items[10], {"ID": 10, "RF": 0.0, "ET": 10, "SL": rbtcs.ITEM_SELECTED_BY_USER, "PR": []})

    def test_handle_seeding_data_misc_seeding(self):
        """ Test that misc seeding is handled correctly"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_misc_seeding.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=100',
                                           '-p', 'Preconditions'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        err_status = rbtcs.validate_data(arguments, data, hdr_row)
        self.assertEqual(err_status, rbtcs.StatusCode.OK)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        err_status = rbtcs.handle_seeding_data(items, arguments, hdr_row)
        self.assertEqual(err_status, rbtcs.StatusCode.OK)
        self.assertEqual(items[0]["SL"], rbtcs.ITEM_SELECTED_BY_USER)
        self.assertEqual(items[1]["SL"], rbtcs.ITEM_SELECTED_BY_USER)
        self.assertEqual(items[1]["PR"], [])
        self.assertEqual(items[2]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)
        self.assertEqual(items[3]["SL"], rbtcs.ITEM_SELECTED_BY_USER)
        self.assertEqual(items[3]["PR"], [])
        self.assertEqual(items[4]["SL"], rbtcs.ITEM_EXCLUDED_BY_USER)
        self.assertEqual(items[5]["SL"], rbtcs.ITEM_SELECTED_BY_USER)
        self.assertEqual(items[6]["SL"], rbtcs.ITEM_EXCLUDED_BY_USER)
        self.assertEqual(items[7]["SL"], rbtcs.ITEM_EXCLUDED_BY_USER)
        self.assertEqual(items[8]["SL"], rbtcs.ITEM_EXCLUDED_BY_USER)
        self.assertEqual(items[9]["SL"], rbtcs.ITEM_SELECTED_BY_USER)
        self.assertEqual(items[10]["SL"], rbtcs.ITEM_NOT_SELECTED_BY_ALG)


# prepare_data_for_writing()
class TestPrepareDataForWriting(unittest.TestCase):
    """Unit tests for prepare_data_for_writing()    """
    def test_prepare_data(self):
        """ Unit test for prepare_data_for_writing() """
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_validate_data_prerequisites.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        items[1]["SL"] = 1
        items[2]["SL"] = 0
        items[3]["SL"] = 1
        items[9]["SL"] = 0
        rbtcs.prepare_data_for_writing(arguments, data, hdr_row, items)
        pr = data[hdr_row].index(arguments.prerequisites)
        sl = data[hdr_row].index(arguments.selection)
        self.assertEqual(data[hdr_row + 2][pr], '1')
        self.assertEqual(data[hdr_row + 2][sl], 'y')
        self.assertEqual(data[hdr_row + 3][pr], '')
        self.assertEqual(data[hdr_row + 3][sl], 'n')
        self.assertEqual(data[hdr_row + 4][pr], '1,2')
        self.assertEqual(data[hdr_row + 4][sl], 'y')
        self.assertEqual(data[hdr_row + 10][pr], '1,2,3,4,5,6')
        self.assertEqual(data[hdr_row + 10][sl], 'n')

    def test_prepare_data_seeding(self):
        """ Unit test for prepare_data_for_writing() with seeding """
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_misc_seeding.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b=1000',
                                           '-p', 'Preconditions'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        ret = rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rbtcs.handle_seeding_data(items, arguments, hdr_row)
        # no any algorithms involved
        rbtcs.prepare_data_for_writing(arguments, data, hdr_row, items)
        pr = data[hdr_row].index(arguments.prerequisites)
        sl = data[hdr_row].index(arguments.selection)
        self.assertEqual(data[hdr_row + 1][pr], '')
        self.assertEqual(data[hdr_row + 1][sl], 'y')
        self.assertEqual(data[hdr_row + 2][pr], '1')
        self.assertEqual(data[hdr_row + 2][sl], 'y')
        self.assertEqual(data[hdr_row + 3][pr], '')
        self.assertEqual(data[hdr_row + 3][sl], 'n')
        self.assertEqual(data[hdr_row + 4][pr], '1,2,10')
        self.assertEqual(data[hdr_row + 4][sl], 'y')
        self.assertEqual(data[hdr_row + 5][pr], '1')
        self.assertEqual(data[hdr_row + 5][sl], 'n')
        self.assertEqual(data[hdr_row + 6][pr], '')
        self.assertEqual(data[hdr_row + 6][sl], 'y')
        self.assertEqual(data[hdr_row + 7][pr], '')
        self.assertEqual(data[hdr_row + 7][sl], 'n')
        self.assertEqual(data[hdr_row + 8][pr], '7')
        self.assertEqual(data[hdr_row + 8][sl], 'n')
        self.assertEqual(data[hdr_row + 9][pr], '8')
        self.assertEqual(data[hdr_row + 9][sl], 'n')
        self.assertEqual(data[hdr_row + 10][pr], '')
        self.assertEqual(data[hdr_row + 10][sl], 'y')


# knapsack_01_dynamic_programming(items, budget)
class TestKnapsack01DP(unittest.TestCase):
    """Unit tests for knapsack_01_dynamic_programming"""

    def test_1(self):
        """seed data <test_alg_1.xlsx>, time budget 165"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_1.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b', '165'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_dynamic_programming(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.4550810)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 1)
        self.assertEqual(items[3]["SL"], 1)
        self.assertEqual(items[4]["SL"], 0)
        self.assertEqual(items[5]["SL"], 1)
        self.assertEqual(items[6]["SL"], 0)
        self.assertEqual(items[7]["SL"], 0)
        self.assertEqual(items[8]["SL"], 0)
        self.assertEqual(items[9]["SL"], 0)

    def test_2(self):
        """seed data <test_alg_2.xlsx>, time budget 26"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_2.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b', '26'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_dynamic_programming(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.5604396)
        self.assertEqual(items[0]["SL"], 0)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 1)
        self.assertEqual(items[3]["SL"], 1)
        self.assertEqual(items[4]["SL"], 0)

    def test_3(self):
        """seed data <test_alg_3.xlsx>, time budget 190"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_3.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b', '190'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_dynamic_programming(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.5660377)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 0)
        self.assertEqual(items[3]["SL"], 0)
        self.assertEqual(items[4]["SL"], 1)
        self.assertEqual(items[5]["SL"], 0)

    def test_4(self):
        """seed data <test_alg_4.xlsx>, time budget 50"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_4.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b', '50'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_dynamic_programming(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.5691489)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 0)
        self.assertEqual(items[2]["SL"], 0)
        self.assertEqual(items[3]["SL"], 1)
        self.assertEqual(items[4]["SL"], 0)
        self.assertEqual(items[5]["SL"], 0)
        self.assertEqual(items[6]["SL"], 0)

    def test_5(self):
        """seed data <test_alg_5.xlsx>, time budget 750"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_5.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=750'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_dynamic_programming(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.5290276)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 0)
        self.assertEqual(items[2]["SL"], 1)
        self.assertEqual(items[3]["SL"], 0)
        self.assertEqual(items[4]["SL"], 1)
        self.assertEqual(items[5]["SL"], 0)
        self.assertEqual(items[6]["SL"], 1)
        self.assertEqual(items[7]["SL"], 1)
        self.assertEqual(items[8]["SL"], 1)
        self.assertEqual(items[9]["SL"], 0)
        self.assertEqual(items[10]["SL"], 0)
        self.assertEqual(items[11]["SL"], 0)
        self.assertEqual(items[12]["SL"], 0)
        self.assertEqual(items[13]["SL"], 1)
        self.assertEqual(items[14]["SL"], 1)

    def test_6(self):
        """seed data <test_alg_6.xlsx>, time budget 6405"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_6.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=6405'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_dynamic_programming(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.5228039)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 0)
        self.assertEqual(items[3]["SL"], 1)
        self.assertEqual(items[4]["SL"], 1)
        self.assertEqual(items[5]["SL"], 1)
        self.assertEqual(items[6]["SL"], 0)
        self.assertEqual(items[7]["SL"], 0)
        self.assertEqual(items[8]["SL"], 0)
        self.assertEqual(items[9]["SL"], 1)
        self.assertEqual(items[10]["SL"], 1)
        self.assertEqual(items[11]["SL"], 0)
        self.assertEqual(items[12]["SL"], 1)
        self.assertEqual(items[13]["SL"], 0)
        self.assertEqual(items[14]["SL"], 0)
        self.assertEqual(items[15]["SL"], 1)
        self.assertEqual(items[16]["SL"], 0)
        self.assertEqual(items[17]["SL"], 0)
        self.assertEqual(items[18]["SL"], 0)
        self.assertEqual(items[19]["SL"], 0)
        self.assertEqual(items[20]["SL"], 0)
        self.assertEqual(items[21]["SL"], 1)
        self.assertEqual(items[22]["SL"], 1)
        self.assertEqual(items[23]["SL"], 1)


# knapsack_01_greedy(items, budget)
class TestKnapsack01Greedy(unittest.TestCase):
    """ Unit tests for knapsack_01_greedy(items, budget) """

    def test_1(self):
        """seed data <test_alg_1.xlsx>, time budget 165"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_1.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=165'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.4550810)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 1)
        self.assertEqual(items[3]["SL"], 1)
        self.assertEqual(items[4]["SL"], 0)
        self.assertEqual(items[5]["SL"], 1)
        self.assertEqual(items[6]["SL"], 0)
        self.assertEqual(items[7]["SL"], 0)
        self.assertEqual(items[8]["SL"], 0)
        self.assertEqual(items[9]["SL"], 0)

    def test_2(self):
        """seed data <test_alg_2.xlsx>, time budget 26"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_2.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=26'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.5164835)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 0)
        self.assertEqual(items[2]["SL"], 1)
        self.assertEqual(items[3]["SL"], 0)
        self.assertEqual(items[4]["SL"], 0)

    def test_3(self):
        """seed data <test_alg_3.xlsx>, time budget 190"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_3.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=190'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.5509434)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 0)
        self.assertEqual(items[3]["SL"], 1)
        self.assertEqual(items[4]["SL"], 0)
        self.assertEqual(items[5]["SL"], 0)

    def test_4(self):
        """seed data <test_alg_4.xlsx>, time budget 50"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_4.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=50'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.5425532)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 0)
        self.assertEqual(items[3]["SL"], 0)
        self.assertEqual(items[4]["SL"], 1)
        self.assertEqual(items[5]["SL"], 1)
        self.assertEqual(items[6]["SL"], 0)

    def test_5(self):
        """seed data <test_alg_5.xlsx>, time budget 750"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_5.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=750'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.5228592)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 1)
        self.assertEqual(items[3]["SL"], 0)
        self.assertEqual(items[4]["SL"], 0)
        self.assertEqual(items[5]["SL"], 0)
        self.assertEqual(items[6]["SL"], 1)
        self.assertEqual(items[7]["SL"], 1)
        self.assertEqual(items[8]["SL"], 1)
        self.assertEqual(items[9]["SL"], 0)
        self.assertEqual(items[10]["SL"], 0)
        self.assertEqual(items[11]["SL"], 0)
        self.assertEqual(items[12]["SL"], 0)
        self.assertEqual(items[13]["SL"], 1)
        self.assertEqual(items[14]["SL"], 1)

    def test_6(self):
        """seed data <test300.xlsx>, time budget 750"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test300.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=15000'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy(items, arguments.time_budget)
        self.assertEquals(rc, 1.0)


# transitive_closure(matr)
class TestTransitiveClosure(unittest.TestCase):
    """ Unit tests for transitive_closure """

    def test_transitive_closure_1(self):
        """test 1"""
        a = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 1, 0], [1, 0, 0, 1, 1]]
        res = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 1, 0], [1, 0, 1, 1, 1]]
        b = rbtcs.transitive_closure(a)
        self.assertEqual(b, res)

    def test_transitive_closure_2(self):
        """test 1"""
        a = [[1, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 0], [1, 0, 1, 1]]
        res = [[1, 0, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
        b = rbtcs.transitive_closure(a)
        self.assertEqual(b, res)

    def test_transitive_closure_3(self):
        """test 1"""
        a = [[1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]
        res = [[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 1, 1]]
        b = rbtcs.transitive_closure(a)
        self.assertEqual(b, res)


# get_preconditions_matrix(items)
class TestGetPreconditionsMatrix(unittest.TestCase):

    def test_get_preconditions_matrix_1(self):
        """test 1"""
        items = [{"ID": 1, "RF": 5.0, "ET": 10, "SL": 0, "PR": [6]},
                 {"ID": 2, "RF": 2.0, "ET": 1, "SL": 0, "PR": [1]},
                 {"ID": 3, "RF": 4.0, "ET": 4, "SL": 0, "PR": [2]},
                 {"ID": 4, "RF": 1.0, "ET": 1, "SL": 0, "PR": [6]},
                 {"ID": 5, "RF": 1.0, "ET": 1, "SL": 0, "PR": [4]},
                 {"ID": 6, "RF": 1.0, "ET": 1, "SL": 0, "PR": []}]

        pc_matrix = rbtcs.get_preconditions_matrix(items)
        self.assertEqual(pc_matrix, [[1, 0, 0, 0, 0, 1], [1, 1, 0, 0, 0, 1], [1, 1, 1, 0, 0, 1],
                                     [0, 0, 0, 1, 0, 1], [0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 1]])


# get_cumulative_ratio_and_cost(items, prereq_matr)
class TestCumulativeRatio(unittest.TestCase):
    """ Unit tests for get_cumulative_ratio_and_cost(items, prereq_matr) """

    def test_cumulative_ratio_1(self):
        """test 1"""
        items = [{"ID": 0, "RF": 5.0, "ET": 10, "SL": 0, "PR": []},
                 {"ID": 1, "RF": 2.0, "ET": 1, "SL": 0, "PR": [1]}]
        prereq_matr = [[1, 0], [1, 1]]
        cumulative_ratio = rbtcs.get_cumulative_ratio_and_cost(items, prereq_matr)
        self.assertEqual(cumulative_ratio[0]["CRATIO"], 0.5)
        self.assertEqual(cumulative_ratio[0]["CCOST"], 10)
        self.assertAlmostEqual(cumulative_ratio[1]["CRATIO"], 0.6363636)
        self.assertEqual(cumulative_ratio[1]["CCOST"], 11)

    def test_cumulative_ratio_2(self):
        """test 2"""
        items = [{"ID": 0, "RF": 5.0, "ET": 10, "SL": 0, "PR": []},
                 {"ID": 1, "RF": 2.0, "ET": 1, "SL": 0, "PR": [1]},
                 {"ID": 2, "RF": 4.0, "ET": 4, "SL": 0, "PR": [0]},
                 {"ID": 3, "RF": 1.0, "ET": 1, "SL": 0, "PR": [1, 2, 3]}]

        prereq_matr = [[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [1, 1, 1, 1]]
        cumulative_ratio = rbtcs.get_cumulative_ratio_and_cost(items, prereq_matr)
        self.assertEqual(cumulative_ratio[0]["CRATIO"], 0.5)
        self.assertAlmostEqual(cumulative_ratio[1]["CRATIO"], 0.6363636)
        self.assertAlmostEqual(cumulative_ratio[2]["CRATIO"], 1.0)
        self.assertAlmostEqual(cumulative_ratio[3]["CRATIO"], 0.75)

    def test_cumulative_ratio_3(self):
        """test 1"""
        items = [{"ID": 0, "RF": 0.0, "ET": 0, "SL": 0, "PR": []},
                 {"ID": 1, "RF": 2.0, "ET": 1, "SL": 0, "PR": [1]}]
        prereq_matr = [[1, 0], [1, 1]]
        cumulative_ratio = rbtcs.get_cumulative_ratio_and_cost(items, prereq_matr)
        self.assertEqual(cumulative_ratio[0]["CRATIO"], 0.0)
        self.assertEqual(cumulative_ratio[0]["CCOST"], 0)
        self.assertAlmostEqual(cumulative_ratio[1]["CRATIO"], 2.0)
        self.assertEqual(cumulative_ratio[1]["CCOST"], 1)


# knapsack_01_greedy_preconditions(items, budget)
class TestKnapsack01GreedyPrerequisites(unittest.TestCase):
    """ Unit tests for knapsack_01_greedy_preconditions(items, budget) """

    def test_1(self):
        """seed data <test_greedy_prerequisites_1.xlsx>, time budget 56"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_greedy_prerequisites_1.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b', '56',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy_preconditions(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 1.0)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 1)
        self.assertEqual(items[3]["SL"], 1)
        self.assertEqual(items[4]["SL"], 1)
        self.assertEqual(items[5]["SL"], 1)
        self.assertEqual(items[6]["SL"], 1)
        self.assertEqual(items[7]["SL"], 1)
        self.assertEqual(items[8]["SL"], 1)
        self.assertEqual(items[9]["SL"], 1)

    def test_2(self):
        """seed data <test_greedy_prerequisites_1.xlsx>, time budget 40"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_greedy_prerequisites_1.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b', '40',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy_preconditions(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.7562879)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 1)
        self.assertEqual(items[3]["SL"], 1)
        self.assertEqual(items[4]["SL"], 1)
        self.assertEqual(items[5]["SL"], 0)
        self.assertEqual(items[6]["SL"], 0)
        self.assertEqual(items[7]["SL"], 1)
        self.assertEqual(items[8]["SL"], 1)
        self.assertEqual(items[9]["SL"], 0)

    def test_3(self):
        """ Test single walk case"""
        items = [{"ID":1, "RF": 1.0, "ET": 1, "SL": 0, "PR": []},
                 {"ID":2, "RF": 2.0, "ET": 2, "SL": 0, "PR": []},
                 {"ID":3, "RF": 10.0, "ET": 1, "SL": 0, "PR": [1, 2]}]
        rc = rbtcs.knapsack_01_greedy_preconditions(items, 4)
        self.assertAlmostEqual(rc, 1.0)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 1)

    def test_4(self):
        """seed data <test_greedy_prerequisites_2.xlsx>, time budget 60"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_greedy_prerequisites_2.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b', '60',
                                           '-p', 'Prerequisites'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy_preconditions(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.87473904)
        self.assertEqual(items[0]["SL"], 0)
        self.assertEqual(items[1]["SL"], 0)
        self.assertEqual(items[2]["SL"], 1)
        self.assertEqual(items[3]["SL"], 1)
        self.assertEqual(items[4]["SL"], 0)
        self.assertEqual(items[5]["SL"], 0)
        self.assertEqual(items[6]["SL"], 1)
        self.assertEqual(items[7]["SL"], 1)
        self.assertEqual(items[8]["SL"], 1)
        self.assertEqual(items[9]["SL"], 1)

    def test_cyclic_preconditions(self):
        """seed data <test_greedy_cyclic_preconditions.xlsx>, time budget 78 and 79"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_greedy_cyclic_preconditions.xlsx',
                                           '-r', 'Risk Values',
                                           '-t', 'EXECost (MH)',
                                           '-s', 'Covered (n)?',
                                           '-b', '78',
                                           '-p', 'Preconditions'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy_preconditions(items, arguments.time_budget)
        self.assertAlmostEqual(rc, 0.0)
        self.assertEqual(items[0]["SL"], 0)
        self.assertEqual(items[1]["SL"], 0)
        self.assertEqual(items[2]["SL"], 0)
        self.assertEqual(items[3]["SL"], 0)
        self.assertEqual(items[4]["SL"], 0)
        self.assertEqual(items[5]["SL"], 0)
        self.assertEqual(items[6]["SL"], 0)
        self.assertEqual(items[7]["SL"], 0)
        self.assertEqual(items[8]["SL"], 0)
        self.assertEqual(items[9]["SL"], 0)
        self.assertEqual(items[10]["SL"], 0)
        self.assertEqual(items[11]["SL"], 0)
        self.assertEqual(items[12]["SL"], 0)
        self.assertEqual(items[13]["SL"], 0)
        self.assertEqual(items[14]["SL"], 0)

        items = rbtcs.extract_items(arguments, data, hdr_row)
        rc = rbtcs.knapsack_01_greedy_preconditions(items, arguments.time_budget+1)
        self.assertAlmostEqual(rc, 1.0)
        self.assertEqual(items[0]["SL"], 1)
        self.assertEqual(items[1]["SL"], 1)
        self.assertEqual(items[2]["SL"], 1)
        self.assertEqual(items[3]["SL"], 1)
        self.assertEqual(items[4]["SL"], 1)
        self.assertEqual(items[5]["SL"], 1)
        self.assertEqual(items[6]["SL"], 1)
        self.assertEqual(items[7]["SL"], 1)
        self.assertEqual(items[8]["SL"], 1)
        self.assertEqual(items[9]["SL"], 1)
        self.assertEqual(items[10]["SL"], 1)
        self.assertEqual(items[11]["SL"], 1)
        self.assertEqual(items[12]["SL"], 1)
        self.assertEqual(items[13]["SL"], 1)
        self.assertEqual(items[14]["SL"], 1)


class TestOptimalAlgorithms(unittest.TestCase):
    """Unit tests for all implementations of algorithms with optimal solution"""

    def test_1(self):
        """seed data <test_alg_1.xlsx>, time budget 165"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_1.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b', '165'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_dynamic_programming_01(arguments, data, hdr_row)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [92.0, 23, 1], [57.0, 31, 1], [49.0, 29, 1],
             [68.0, 44, 1], [60.0, 53, 0], [43.0, 38, 1], [67.0, 63, 0], [84.0, 85, 0], [87.0, 89, 0], [72.0, 82, 0]]
        self.assertEquals(data, sol)

    def test_2(self):
        """seed data <test_alg_2.xlsx>, time budget 26"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_2.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b', '26'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_dynamic_programming_01(arguments, data, hdr_row)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [24.0, 12, 0], [13.0, 7, 1],
               [23.0, 11, 1], [15.0, 8, 1], [16.0, 9, 0]]
        self.assertEquals(data, sol)

    def test_3(self):
        """seed data <test_alg_3.xlsx>, time budget 190"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_3.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b', '190'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_dynamic_programming_01(arguments, data, hdr_row)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [50.0, 56, 1],
               [50.0, 59, 1], [64.0, 80, 0], [46.0, 64, 0], [50.0, 75, 1], [5.0, 17, 0]]
        self.assertEquals(data, sol)

    def test_4(self):
        """seed data <test_alg_4.xlsx>, time budget 50"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_4.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b', '50'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_dynamic_programming_01(arguments, data, hdr_row)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [70.0, 31, 1], [20.0, 10, 0],
               [39.0, 20, 0], [37.0, 19, 1], [7.0, 4, 0], [5.0, 3, 0], [10.0, 6, 0]]
        self.assertEquals(data, sol)

    def test_5(self):
        """seed data <test_alg_5.xlsx>, time budget 750"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_5.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=750'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_dynamic_programming_01(arguments, data, hdr_row)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [135.0, 70, 1], [139.0, 73, 0], [149.0, 77, 1],
               [150.0, 80, 0], [156.0, 82, 1], [163.0, 87, 0], [173.0, 90, 1], [184.0, 94, 1], [192.0, 98, 1],
               [201.0, 106, 0], [210.0, 110, 0], [214.0, 113, 0], [221.0, 115, 0], [229.0, 118, 1], [240.0, 120, 1]]
        self.assertEquals(data, sol)

    def test_6(self):
        """seed data <test_alg_6.xlsx>, time budget 6405"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_6.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=6405'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_dynamic_programming_01(arguments, data, hdr_row)
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
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=165'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_greedy_01(arguments, data, hdr_row)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [92.0, 23, 1], [57.0, 31, 1], [49.0, 29, 1],
             [68.0, 44, 1], [60.0, 53, 0], [43.0, 38, 1], [67.0, 63, 0], [84.0, 85, 0], [87.0, 89, 0], [72.0, 82, 0]]
        self.assertEquals(data, sol)

    def test_2(self):
        """seed data <test_alg_2.xlsx>, time budget 26"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_2.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=26'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_greedy_01(arguments, data, hdr_row)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [24.0, 12, 1], [13.0, 7, 0],
               [23.0, 11, 1], [15.0, 8, 0], [16.0, 9, 0]]
        self.assertEquals(data, sol)

    def test_3(self):
        """seed data <test_alg_3.xlsx>, time budget 190"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_3.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=190'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_greedy_01(arguments, data, hdr_row)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [50.0, 56, 1],
               [50.0, 59, 1], [64.0, 80, 0], [46.0, 64, 1], [50.0, 75, 0], [5.0, 17, 0]]
        self.assertEquals(data, sol)

    def test_4(self):
        """seed data <test_alg_4.xlsx>, time budget 50"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_4.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=50'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_greedy_01(arguments, data, hdr_row)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [70.0, 31, 1], [20.0, 10, 1],
               [39.0, 20, 0], [37.0, 19, 0], [7.0, 4, 1], [5.0, 3, 1], [10.0, 6, 0]]
        self.assertEquals(data, sol)

    def test_5(self):
        """seed data <test_alg_5.xlsx>, time budget 750"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test_alg_5.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=750'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        rbtcs.alg_greedy_01(arguments, data, hdr_row)
        sol = [[u'Risk Factor', u'Execution Time', u'Selected'], [135.0, 70, 1], [139.0, 73, 1], [149.0, 77, 1],
               [150.0, 80, 0], [156.0, 82, 0], [163.0, 87, 0], [173.0, 90, 1], [184.0, 94, 1], [192.0, 98, 1],
               [201.0, 106, 0], [210.0, 110, 0], [214.0, 113, 0], [221.0, 115, 0], [229.0, 118, 1], [240.0, 120, 1]]
        self.assertEquals(data, sol)

    def test_6(self):
        """seed data <test300.xlsx>, time budget 750"""
        arguments = rbtcs.parse_arguments([rbtcs.default_arguments['rbtcs'],
                                           'test300.xlsx',
                                           '-r', 'Risk Factor',
                                           '-t', 'Execution Time',
                                           '-s', 'Selected',
                                           '-b=15000'])
        data = rbtcs.read_data(arguments.filename)
        hdr_row = rbtcs.detect_header_row(arguments, data)
        rbtcs.validate_data(arguments, data, hdr_row)
        a = rbtcs.alg_greedy_01(arguments, data, hdr_row)
        self.assertEquals(a, 1.0)


class TestValidateFilename(unittest.TestCase):
    """Unit tests for validate_filename()"""

    def test_valide_filename_valid(self):
        """unit test for valid file name"""
        res = rbtcs.validate_filename('test_alg_1.xlsx')
        self.assertEquals(res, rbtcs.StatusCode.OK)

    def test_valide_filename_invalid(self):
        """unit test for invalid file name"""
        res = rbtcs.validate_filename('trash.trash')
        self.assertEquals(res, rbtcs.StatusCode.ERR_FILE_NOT_FOUND)

if __name__ == '__main__':
    unittest.main()
