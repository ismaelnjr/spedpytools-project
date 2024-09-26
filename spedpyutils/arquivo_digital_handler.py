import pandas as pd
from xsdata.formats.dataclass.parsers import XmlParser
from spedpyutils.biddings.hierarquical_schema import HierarquicalSchema
from collections import OrderedDict
from sped.arquivos import ArquivoDigital
from sped.registros import Registro
from sped.campos import Campo
from tqdm import tqdm
import importlib
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')



class ArquivoDigitalHandler(object):
    _dataframes = None
    _schema = None
    _arquivo_digital = None
    
    def __init__(self, arq: ArquivoDigital, schema: HierarquicalSchema):
        self._dataframes = None
        self._schema = schema
        self._arquivo_digital = arq   
    
    def __init__(self, arq: ArquivoDigital, schema_path: str):
        self._dataframes = None
        self._schema = self._load_schema(schema_path)
        self._arquivo_digital = arq   

    def getDataFrame(self, registro_id: str):
        self.update()
        return self._dataframes[registro_id]
    
    def getContent(self) -> OrderedDict:
        return self._dataframes

    def _read_data(self) -> OrderedDict:
        
        df = OrderedDict()
        cache = {}
        table_map = self._create_table_map(self._schema)
             
        for registro in tqdm(self._extract_content(self._arquivo_digital), 
                      desc="processing dataframe", 
                      colour="RED"):
            
            if registro.REG in table_map.keys():
                
                # mantendo cache do ultimo registro lido com campos chaves
                r_keys_vals = []
                r_keys_cols = table_map[registro.REG][1]
                for kcol in r_keys_cols:
                    r_keys_vals.append(self._get_registro_value(registro, kcol))
                if len(r_keys_cols) > 0:
                    cache[registro.REG] = [r_keys_cols, r_keys_vals]
            
                # montando a linha do registro concatenando informações relativa ao pai                
                r_parent = table_map[registro.REG][2]
                r_cols = [registro.REG] + table_map[registro.REG][0]
                r_vals = []
                
                for col in r_cols:
                    r_vals.append(self._get_registro_value(registro, col))
                
                if r_parent:
                    while not r_parent == None:
                        r_cols = [r_parent] + cache[r_parent][0] + r_cols
                        r_vals = [r_parent] + cache[r_parent][1] + r_vals
                        r_parent = table_map[r_parent][2]

                if not registro.REG in df.keys():
                    df[registro.REG] = pd.DataFrame(columns=self._get_cols_names(r_cols))
                
                df[registro.REG].loc[len(df[registro.REG])] = r_vals
        
        return df
    
    def _get_cols_names(self, cols: any):
        array = []
        for col in cols:
            if isinstance(col, Campo):
                    array.append(col.nome)
            else:
                array.append(col)
        return array

    
    def _get_registro_value(self, registro: Registro, obj:  any):
        if isinstance(obj, Campo): 
            return getattr(registro, obj.nome)
        else:                    
            return str(obj)
    
    def _extract_content(self, arq: ArquivoDigital):         
        array = []
        for key in arq._blocos.keys():
            array += arq._blocos[key]._registros
        return [arq._registro_abertura] + array + [arq._registro_encerramento]

    def  _create_table_map(self, schema: HierarquicalSchema): 
        map = {}
        for table_list in schema.table_list:         
            
            for table in table_list.table:            
                all_columns_dict = self._get_all_cols_dict(schema, table)   
                
                cols, idx_cols, idx_names = [], [], []
            
                if table.index != None:
                    idx_names = table.index.split("|")
                    
                for col in table.column:
                    if '__all__' == col.name:
                        cols = list(all_columns_dict.values())                    
                    else:
                        cols.append(all_columns_dict.get(col.name))      
                
                for idx in idx_names:
                    idx_cols.append(all_columns_dict.get(idx))
                                    
                map[table.id] = (cols, idx_cols, table.parent)
                
        return map
    
    def _get_all_cols_dict(self, schema: HierarquicalSchema, table: HierarquicalSchema.TableList.Table):
        dict = {}
        try:
            modulo = importlib.import_module(f"{schema.clazz_path}.registros")
            clazz = getattr(modulo, f"Registro{table.id}")
            for col in getattr(clazz, 'campos'):
                if col.nome != 'REG':
                    dict[col.nome] = col
        except ImportError:
            print(f"Erro: O módulo '{modulo}' não foi encontrado.")
        except AttributeError:
            print(f"Erro: A classe '{clazz}' não foi encontrada no módulo '{modulo}'.")
        
        return dict
        
         
    def to_excel(self, filename):
        try:
            self.update()
            with pd.ExcelWriter(filename) as writer:
                # Exportar registros por aba
                for tab_list in tqdm(self._schema.table_list, 
                                desc="exporting data", 
                                colour="RED"):
                    for tab in tab_list.table:
                        df = self._dataframes[tab.id] 
                        if not tab.exclude:                            
                            df.to_excel(writer, index=False, sheet_name=tab.id, engine='openpyxl')
                                            
        except Exception as e:
            raise RuntimeError(f"Erro não foi possível exportar dados para arquivo: {filename}, erro: {e}")

    def update(self, reload: bool = False):        
        if self._dataframes is None or reload:
            self._dataframes = self._read_data()

    def _load_schema(self, name):
        parser = XmlParser()
        return parser.parse(name, HierarquicalSchema)
