import unittest
import os
import sys
import json

dir = os.path.dirname(__file__)
path = os.path.join(dir, '../..')
sys.path.insert(0, path)

# Here is the graph contained in pruning.xlsx
#       
#                          test
#                         /  |  \
#      A1 B1 C1   D1    G1  H1  I1
#       \  \ /    /       \  |  /
#       A2 B2   D2          H2
#         \/    /          /  
#         A3   /          /
#           \ /          /
#           C6__________/
#      
from koala import ExcelCompiler


class Test_without_range(unittest.TestCase):
    
    def setUp(self):
        file_name = "./tests/ast/pruning.xlsx"

        c = ExcelCompiler(file_name)
        sp = c.gen_graph(outputs = ["Sheet1!C6"])
        sp =sp.prune_graph(["Sheet1!A1","Sheet1!B1"])
        self.sp = sp
        
    def test_pruning_nodes(self):
    	self.assertEqual(self.sp.G.number_of_nodes(), 9)

    def test_pruning_edges(self):
        self.assertEqual(self.sp.G.number_of_edges(), 8)

    def test_pruning_cellmap(self):
        self.assertEqual(len(self.sp.cellmap.keys()), 9)

    def test_eval(self):
        self.sp.set_value('Sheet1!A1', 10)
        self.assertEqual(self.sp.evaluate('Sheet1!C6'), 38)

class Test_with_range(unittest.TestCase):
    
    def setUp(self):
        file_name = "./tests/ast/pruning.xlsx"

        c = ExcelCompiler(file_name)
        sp = c.gen_graph(outputs = ["Sheet1!C6"])
        sp = sp.prune_graph(["Sheet1!A1","Sheet1!B1", "test"])
        self.sp = sp

    def test_pruning_nodes(self):
      self.assertEqual(self.sp.G.number_of_nodes(), 13)

    def test_pruning_edges(self):
        self.assertEqual(self.sp.G.number_of_edges(), 12)

    def test_pruning_cellmap(self):
        self.assertEqual(len(self.sp.cellmap.keys()), 13)

    def test_A1(self):
        self.sp.set_value('Sheet1!A1', 10)
        self.assertEqual(self.sp.evaluate('Sheet1!C6'), 38)

    def test_H1(self):
        self.sp.set_value('Sheet1!H1', 4)
        self.assertEqual(self.sp.evaluate('Sheet1!C6'), 31)

    def test_G1(self):
        self.sp.set_value('test', 4)
        self.assertEqual(self.sp.evaluate('Sheet1!C6'), 35)

    def test_G1_bis(self):
        self.sp.set_value('test', [7,8,9])
        self.assertEqual(self.sp.evaluate('Sheet1!C6'), 47)

if __name__ == '__main__':
    unittest.main()


