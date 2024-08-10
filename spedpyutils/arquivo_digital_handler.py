import pandas as pd
from xsdata.formats.dataclass.parsers import XmlParser
from spedpyutils.biddings.hierarquical_schema import HierarquicalSchema
from collections import OrderedDict
from sped.arquivos import ArquivoDigital
from sped.registros import Registro

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class ArquivoDigitalHandler(object):

    def __init__(self, arq: ArquivoDigital, schema: HierarquicalSchema):
        self._dataframes = None
        self._schema = schema
        self._arquivo_digital = arq   
    
    def __init__(self, arq: ArquivoDigital, schema_path: str):
        self._dataframes = None
        self._schema = self._load_schema(schema_path)
        self._arquivo_digital = arq   

    def getTable(self, registro_id: str):
        self.refresh()
        return self._dataframes[registro_id]
    
    def getAllTables(self) -> OrderedDict:
        return self._dataframes

    def _read_data(self) -> OrderedDict:
        
        df = OrderedDict()
        cache = {}
        map = self._create_cols_map(self._schema)
             
        for r in self._extract_content(self._arquivo_digital):
            
            if r.REG in map.keys():
                
                # mantendo cache do ultimo registro lido com campos chaves
                r_keys_vals = []
                r_keys_cols = map[r.REG][1]
                for c in r_keys_cols:
                    r_keys_vals.append(self._get_registro_value(r, c))
                if len(r_keys_cols) > 0:
                    cache[r.REG] = [r_keys_cols, r_keys_vals]
            
                # montando a linha do registro concatenando informações relativa ao pai                
                r_parent = map[r.REG][2]
                r_cols = [r.REG] + map[r.REG][0]
                r_vals = []
                
                for c in r_cols:
                    r_vals.append(self._get_registro_value(r, c))
                
                if r_parent:
                    while not r_parent == None:
                        r_cols = [r_parent] + cache[r_parent][0] + r_cols
                        r_vals = [r_parent] + cache[r_parent][1] + r_vals
                        r_parent = map[r_parent][2]

                if not r.REG in df.keys():
                    df[r.REG] = pd.DataFrame(columns=self._getColumnNames(r_cols))
                
                df[r.REG].loc[len(df[r.REG])] = r_vals
        
        return df
    
    def _getColumnNames(self, cols: any):
        array = []
        for c in cols:
            if isinstance(c, HierarquicalSchema.TablesList.Table.Column):
                array.append(c.name)
            else:
                array.append(c)
        return array

    
    def _get_registro_value(self, r: Registro, c:  any):
            if isinstance(c, HierarquicalSchema.TablesList.Table.Column):
                value = getattr(r, c.name)
                if "datetime" == c.type_value:
                    try:
                        return value.strftime(c.dateformat)
                    except:
                        return value
                elif "decimal" == c.type_value:
                    try:
                        return locale.format_string("%.2f", value)
                    except:
                        return value
                else:
                    return value
            else:
                return c
    
    def _extract_content(self, arq: ArquivoDigital):         
        array = []
        for key in arq._blocos.keys():
            array += arq._blocos[key]._registros
        return [arq._registro_abertura] + array + [arq._registro_encerramento]

    def  _create_cols_map(self, schema: HierarquicalSchema): 
        map = {}
        for t in schema.tables_list.table:
            cols, index, idx_names = [], [], []
            if t.index != None:
                idx_names = t.index.split("|")
            for c in t.column:
                cols.append(c)      
                if c.name in idx_names:
                    index.append(c)             
            map[t.id] = (cols, index, t.parent)
        return map
         
    def to_excel(self, filename):
        try:
            self.refresh()
            with pd.ExcelWriter(filename) as writer:
                # Exportar registros por aba   
                for key in self._dataframes:
                    df = self._dataframes[key]      
                    df.to_excel(writer, index=False, sheet_name=key, engine='openpyxl')
                                            
        except Exception as e:
            raise RuntimeError(f"Erro não foi possível exportar dados para arquivo: {filename}, erro: {e}")

    def refresh(self, force_reload: bool = False):        
        if self._dataframes is None or force_reload:
            self._dataframes = self._read_data()

    def _load_schema(self, name):
        parser = XmlParser()
        return parser.parse(name, HierarquicalSchema)
