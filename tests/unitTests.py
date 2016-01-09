#!/usr/bin/env python
# encoding=utf-8

import unittest

def suite():
    # modules_to_test = ('asBuilderTests', 'asModelTests') # and so on
    modules_to_test = (
        'test_package', 'test_class',
        'test_class_field', 'test_class_method',
        'test_builder', 'test_parsing_files',
    )  # and so on
    alltests = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
