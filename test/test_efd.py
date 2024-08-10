import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from sped.efd.icms_ipi.arquivos import ArquivoDigital
from spedpyutils.biddings.hierarquical_schema import HierarquicalSchema
from spedpyutils.arquivo_digital_handler import ArquivoDigitalHandler

class TestEFD(unittest.TestCase):

    def test_read_registro(self):
        
        arq = ArquivoDigital()
        arq.readfile("efd.txt")

        test = ArquivoDigitalHandler(arq, "schema-sample1.xml")
        test.to_excel("output.xlsx")
        df = test.getTable("C170")
        self.assertEqual("TESTE LTDA", arq._registro_abertura.NOME)
        self.assertEqual("24672", df["NUM_DOC"][1])

if __name__ == '__main__':
    unittest.main()