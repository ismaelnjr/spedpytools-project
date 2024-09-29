from pathlib import Path
from sped.efd.icms_ipi.arquivos import ArquivoDigital as EFDArquivoDigital
from sped.nfe.arquivos import ArquivoDigital as NFeArquivoDigital
from .arquivo_digital_handler import ArquivoDigitalHandler


class SpedPyTools:      
    """
    A utility class for handling SPED (Public Digital Bookkeeping System) files.
    """
    
    __EFD_ICMS_IPI_LAYOUT__ = 'layout/efd_icms_ipi_layout.json'
    __NFE_LAYOUT__ = 'layout/nfe_rep_layout.json'
    
    class EFDFile(EFDArquivoDigital):
        """
        A class for managing EFD data and exporting it to Excel.

        This class initializes the ArquivoDigitalHandler with the EFD schema and provides 
        a method to export the EFD data to an Excel file.

        Methods:
            to_excel(filename): Exports the EFD data to the specified Excel file.

        Examples:
            efd_instance = SpedPyTools.EFD()
            efd_instance.readfile("efd.txt")
            efd_instance.to_excel("efd_output.xlsx")
        """
        
        def __init__(self):
            super().__init__()
            layout_path = Path(__file__).parent / SpedPyTools.__EFD_ICMS_IPI_LAYOUT__
            self._handler = ArquivoDigitalHandler(self, str(layout_path))

        def to_excel(self, filename: str, verbose = False):
            """
            Exports the EFD data to an Excel file.

            This method reads the EFD data using the handler and then exports it to the 
            specified Excel file.

            Args:
                filename (str): The name of the Excel file to which the EFD data will be exported.
 
            """
            self._handler.build_dataframes(verbose=verbose)
            self._handler.to_excel(filename, verbose=verbose)
    
    class NFeFile(NFeArquivoDigital):
        """
        A class for managing NFe data and exporting it to Excel.

        This class initializes the ArquivoDigitalHandler with the NFe schema and provides 
        a method to export the EFD data to an Excel file.

        Methods:
            to_excel(filename): Exports the NFe data to the specified Excel file.

        Examples:
            nfeRep_instance = SpedPyTools.NFeFileRep()
            nfeRep_instance.readfile("nfe.txt")
            nfeRep_instance.to_excel("nfe_output.xlsx")
        """
        
        def __init__(self):
            super().__init__()
            layout_path = Path(__file__).parent / SpedPyTools.__NFE_LAYOUT__
            self._handler = ArquivoDigitalHandler(self, str(layout_path))

        def to_excel(self, filename: str, verbose = False):
            """
            Exports the NFe data to an Excel file.

            This method reads the NFe data using the handler and then exports it to the 
            specified Excel file.

            Args:
                filename (str): The name of the Excel file to which the NFe data will be exported.
 
            """
            self._handler.build_dataframes(verbose=verbose)
            self._handler.to_excel(filename, verbose=verbose)
