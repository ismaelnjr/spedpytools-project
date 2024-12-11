import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from sped.nfe.arquivos import ArquivoDigital as ArquivoDigital
from spedpytools import ArquivoDigitalSchema, ArquivoDigitalHandler

class TestNFeRep(unittest.TestCase):

    def test_read_and_export(self):
        
        txt = """|0000|TESTE LTDA|23004906000180|
|N001|1|
|N100|23004906000180|TESTE LTDA|135418|1|02052024|SAIDA|35240523004906000180550010001354181002078142|23.004.906/0001-80||DANIELA EVANGELISTA DA SILVA|BA|80,00|05_2024|27092024|AUTORIZADA|||
|N170|23004906000180|135418|1|1|AERCX02RD|CAIXA DE SOM BLUETOOTH COR VERMELHO CARMIM AERBOX 2|85182100|2949|80,00|1,0000|UN|80,00|0,00|0,00|0,00|0,00|80,00|||80,00|4,00|3,20|0,00|0,00|0,00|0,00|03|0,00|
|N141|135418A|02052024|80,00|
|N990|3|
|Z001|1|
|Z100|23004906000180||35240523004906000180550010001354181002078142|02052024|10111|Cancelamento|Valor errado|PROT1111|
|Z990|0|
|9999|2|
"""
        with open('output\\nfe.txt', 'w') as f:
            f.write(txt)
        
        arq = ArquivoDigital()
        arq.readfile('output\\nfe.txt')        
        schema = ArquivoDigitalSchema('etc\schema_nfe.json')
        export = ArquivoDigitalHandler(schema=schema, arquivo_digital=arq)        
        export.to_excel("output\\nfe_output.xlsx")
               
if __name__ == '__main__':
    unittest.main()