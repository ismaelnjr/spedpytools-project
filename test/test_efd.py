import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from spedpyutils.sped_utils import SpedUtils

class TestEFD(unittest.TestCase):

    def test_read_registro(self):
        
        arq = SpedUtils.EFD()
        arq.readfile("efd.txt")
        arq.to_excel("output.xlsx", verbose=True)
               
if __name__ == '__main__':
    unittest.main()