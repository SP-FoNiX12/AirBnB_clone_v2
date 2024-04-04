#!/usr/bin/python3
""" Module doc"""
import unittest
import console


class test_Console(unittest.TestCase):
    """ document documt """

    def test_documentation(self):
        """ document documt """
        self.assertIsNotNone(console.__doc__)
