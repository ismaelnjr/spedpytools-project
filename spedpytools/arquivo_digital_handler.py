from collections import OrderedDict
from sped.arquivos import ArquivoDigital
from sped.registros import Registro
from sped.campos import Campo, CampoNumerico
from tqdm import tqdm
import pandas as pd
import importlib
import json
import itertools


class ArquivoDigitalHandler:
    """
    Handles the processing and management of digital file records.

    This class is responsible for loading schemas, building pandas DataFrames from digital file records, 
    and exporting the data to Excel files. It manages hierarchical relationships between records and 
    provides access to the constructed DataFrames.

    Args:
        arquivo_digital (ArquivoDigital): The digital file containing records to be processed.
        layout (ExportLayout): The layout definition used for exporting the records.

    Attributes:
        get_dataframes (OrderedDict): Property that returns the constructed DataFrames.

    Examples:
        handler = ArquivoDigitalHandler(arquivo_digital, schema)
        handler.build_dataframes(silent=False)
        handler.to_excel("output.xlsx")
    """

    def __init__(self, arquivo_digital: ArquivoDigital, config_file: str):
        self._dataframes = None
        self._arquivo_digital = arquivo_digital
        self.__load_export_config(config_file)
            
    def __load_export_config(self, config_file):
        
        with open(config_file, 'r') as f:
            self._config_file = json.load(f)
            
            self._data_source_list = self._config_file.get("data_sources", {})
            self._clazz_path = self._config_file.get("clazz_path", None)
            self._spreadsheet = self._config_file.get("spreadsheet", [])
            self._views = self._config_file.get("views", [])
            self._indexes = {}



    @property
    def get_dataframes(self) -> OrderedDict:
        return self._dataframes

    def build_all(self, verbose: bool = False):
        """
        Retrieves the constructed DataFrames (datasources and views).

        This property provides access to the internal dictionary of DataFrames that have been built 
        from the digital file records. It allows other parts of the code to access the DataFrames 
        without directly manipulating the internal state.

        Returns:
            OrderedDict: The dictionary containing the constructed DataFrames.
        """
        self._dataframes = {}
        self.create_sources(verbose=verbose)
        self.create_views(verbose=verbose)
        return self._dataframes

    def create_sources(self, verbose=True):
        """
        Builds a dictionary of pandas DataFrames from the records in the digital file.

        This method processes each record, extracting relevant columns and values, 
        and organizes them into DataFrames based on their unique identifiers. 
        It also handles hierarchical relationships between records.

        Args:
            verbose (bool): If False, suppresses progress output during processing. Defaults to True.

        Returns:
            None: The method assigns the constructed DataFrames to the instance variable _dataframes.

        Examples:
            handler.sources(verbose=False)
        """
        sources = {}
        cache = {}
        source_map = self.__create_source_map()

        for registro in tqdm(self.__get_all_registros(), 
                            desc="processing dataframe", 
                            colour="RED",
                            disable=not verbose):

            if registro.REG in source_map:
                

                cols = list(source_map[registro.REG][0])
                cols_dict = source_map[registro.REG][1]
                parent = source_map[registro.REG][2]
                
                vals = [self.__get_column_value(registro, col, cols_dict) for col in cols]
                cache[registro.REG] = vals
                
                while parent:
                    vals = vals + cache[parent]
                    cols += [f'{parent}.{parent_col}' for parent_col in source_map[parent][0]]      
                    parent = source_map[parent][2]           
                
                if registro.REG not in sources:
                    sources[registro.REG] = pd.DataFrame(columns=cols)
                    sources[registro.REG] = sources[registro.REG].astype(self.__get_cols_dtypes(cols_dict)) # Definir que campos numericos sejam sempre float 

                sources[registro.REG].loc[len(sources[registro.REG])] = vals
                
        self._dataframes = sources


    def __get_column_value(self, registro: Registro, col: str, cols_dict: dict):
        if col in cols_dict:
            return getattr(registro, cols_dict[col].nome)
        else:
            return self.__get_row_id(registro.REG) if col == '__rowid__' else col

    def __get_row_id(self, idx: str):
        if idx in self._indexes:
            row_id = self._indexes[idx] 
            return next(row_id)
        else:
            self._indexes[idx] = itertools.count(start=1)
            return next(self._indexes[idx])


    def __create_source_map(self): 
        map = {}
        for data_src_id in self._data_source_list: 
            data_source = self._data_source_list.get(data_src_id)
            cols_dict = self.__get_all_cols_dict(data_source)   
            cols = list(cols_dict.keys())
            idx_names = data_source.get('index', '__rowid__').split("|")
                        
            if '__rowid__' in idx_names:
                cols = ['__rowid__'] if cols == [None] else ['__rowid__'] + cols

            map[data_src_id] = (cols, cols_dict, data_source.get('parent', None))

        return map


    def __get_all_cols_dict(self, data_source: any):
        columns_dict = {}
        try:
            modulo = importlib.import_module(self._clazz_path)
            clazz = getattr(modulo, data_source['clazz'])
            columns_dict = {campo.nome: campo for campo in getattr(clazz, 'campos') if campo.nome != 'REG'}
        except ImportError:
            print(f"Erro: O módulo '{modulo}' não foi encontrado.")
        except AttributeError:
            print(f"Erro: A classe '{clazz}' não foi encontrada no módulo '{modulo}'.")
        return columns_dict

    def __get_cols_dtypes(self, cols_dict):
        dtypes = {}
        for col_name in cols_dict:
            col = cols_dict.get(col_name)
            if isinstance(col, CampoNumerico): # definir que campos numericos sejam sempre float64               
                dtypes[col_name] = 'float64'
                
        return dtypes
    
    def create_views(self, verbose=True):

        for view in tqdm(
                self._views,
                desc="gererating data views", 
                colour="RED",
                disable=not verbose
            ):
            
            view_name = view.get('name')
            ldata_source = view.get('data_source', '')
            cols = view.get('columns')

            left_df = self._dataframes.get(ldata_source)

            for join in view.get('joins', []):
                rdata_source = join.get('data_source', '')
                right_df = self._dataframes.get(rdata_source)
                right_df.columns = [f'{rdata_source}.{col}' for col in right_df.columns]
                joinned_df = pd.merge(
                    left=left_df,
                    right=right_df, 
                    left_on=join.get('left_on', f'{rdata_source}.__rowid__'), 
                    right_on=join.get('right_on', '__rowid__'),
                    how=join.get('how', 'inner')) 
                
                left_df = joinned_df                                   

            self._dataframes[view_name] = (left_df if cols == ['__all__'] else left_df[cols])
            

        

    def to_excel(self, filename, verbose = True):
        """
        Exports the constructed DataFrames to an Excel file.

        This method iterates through the schema blocks and their associated records, 
        exporting each DataFrame to a separate sheet in the specified Excel file. 
        It skips any records marked for exclusion.

        Args:
            filename (str): The name of the Excel file to which the data will be exported.
            verbose (bool): If False, suppresses progress output during processing. Defaults to True.

        Raises:
            RuntimeError: If there is an error during the export process, a RuntimeError is raised 
            with a message indicating the failure.

        Examples:
            handler.to_excel("output.xlsx")
        """

        try:
            with pd.ExcelWriter(filename) as writer:
                for tab in tqdm(self._spreadsheet.get("tabs", []),
                                desc="exporting data", 
                                colour="RED",
                                disable=not verbose):
                    view_name = tab.get('view')
                    
                    if view_name in self._dataframes.keys():
                        df = self._dataframes[view_name] 
                        df.to_excel(writer, index=False, sheet_name=tab['name'], engine='openpyxl')  

        except Exception as ex:
            raise RuntimeError(
                f"Erro não foi possível exportar dados para arquivo: {filename}, erro: {ex}"
            ) from ex
    
    def __get_style_output_format(self, cols_dict):
        
        style_format = {}
        for col_name in cols_dict:
            col = cols_dict.get(col_name)
            if isinstance(col, CampoNumerico): 
                style_format[col_name] = ArquivoDigitalHandler.Formatter.txt_to_decimal_br
                
        return style_format
    
    def __get_all_registros(self):        
        array = []
        for key in self._arquivo_digital._blocos:
            array += self._arquivo_digital._blocos[key]._registros
        return [self._arquivo_digital._registro_abertura] + array + [self._arquivo_digital._registro_encerramento]
            

