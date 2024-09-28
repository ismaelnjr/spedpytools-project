import os
from xsdata.formats.dataclass.parsers import XmlParser
from sped.efd.icms_ipi.arquivos import ArquivoDigital as EFDArquivoDigital
from .arquivo_digital_handler import ArquivoDigitalHandler
from .biddings.export_layout import ExportLayout

class SpedUtils:
    """
    A utility class for handling SPED (Public Digital Bookkeeping System) files.
    """

    class EFD(EFDArquivoDigital):
        """
        A class for managing EFD data and exporting it to Excel.

        This class initializes the ArquivoDigitalHandler with the EFD schema and provides 
        a method to export the EFD data to an Excel file.

        Methods:
            to_excel(filename): Exports the EFD data to the specified Excel file.

        Examples:
            efd_instance = SpedUtils.EFD()
            efd_instance.readfile("efd.txt")
            efd_instance.to_excel("efd_output.xlsx")
        """
        
        def __init__(self):
            super().__init__()
            layout_path = os.path.join(os.path.dirname(__file__), 'layout\\export_layout.xml')
            export_layout = XmlParser().parse(layout_path, ExportLayout)
            self._handler = ArquivoDigitalHandler(self, export_layout)

        def to_excel(self, filename: str, verbose = False):
            """
            Exports the EFD data to an Excel file.

            This method reads the EFD data using the handler and then exports it to the 
            specified Excel file.

            Args:
                filename (str): The name of the Excel file to which the EFD data will be exported.
 
            """
            self._handler.build_dataframes(verbose=verbose)
            self._handler.to_excel(filename)
