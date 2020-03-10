import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):

   
    def test_simple(self):
        """More complex program"""
        input = """int main () {
            int a,a;
        }"""
        expect = ""
        self.assertTrue(TestAST.checkASTGen(input,expect,300))