# SPED para python

Biblioteca para visualização de um arquivo sped em estrutura de tabelas do Pandas.
Utiliza o relacionamento hierarquico típico da estrutura do SPED FISCAL (EFD, ECD e entre outros)

A ideia seria visualizar em formato de tabela todas as informações de um registro e seus registros pais, por exemplo:

        from sped.efd.icms_ipi.arquivos import ArquivoDigital
        from spedpyutils.biddings.hierarquical_schema import HierarquicalSchema
        from spedpyutils.arquivo_digital_handler import ArquivoDigitalHandler
        
        arq = ArquivoDigital()        
        arq.readfile("efd.txt") 

        parser = XmlParser()
        schema = parser.parse("schema-sample1.xml", HierarquicalSchema)

        test = ArquivoDigitalHandler(arq, schema)
        #test.to_excel("output.xlsx")
        df = test.getTable("C170")
        print(df)

Resultaria numa saída do tipo:

0000    NOME        DT_INI      DT_FIN      CNPJ                C100    COD_PART    COD_MOD SER NUM_DOC VLR_DOC C170    COD_ITEM    VLR_ITEM
0000    EMPRESAX    01/01/2024  31/01/2024  11.111.111/0001-91  C100    PART1       55      001 1111    1000,00 C170    PRODA       800,00 
0000    EMPRESAX    01/01/2024  31/01/2024  11.111.111/0001-91  C100    PART1       55      001 1111    1000,00 C170    PRODB       200,00 
0000    EMPRESAX    01/01/2024  31/01/2024  11.111.111/0001-91  C100    PART1       55      001 1112    300,00  C170    PRODC       300,00 

Exemplo do arquivo schema-sample1.xml:
"

    <hierarquical-schema name="EFD" version="v1.0">
	<tables-list>
		<table id="0000" description="Abertura" index="DT_INI|DT_FIN">
			<column name="NOME"/>
			<column name="CNPJ"/>
			<column name="UF"/>
			<column name="DT_INI" type="datetime" dateformat="%d/%m/%Y"/>
			<column name="DT_FIN" type="datetime" dateformat="%d/%m/%Y"/>
		</table>
		<table id="C100" description="E_S" parent="0000" index="COD_MOD|SER|NUM_DOC">
			<column name="IND_OPER"/>
			<column name="IND_EMIT"/>
			<column name="COD_PART"/>
			<column name="COD_MOD"/>
			<column name="COD_SIT"/>
			<column name="SER"/>
			<column name="NUM_DOC"/>
			<column name="DT_DOC" type="datetime" dateformat="%d/%m/%Y"/>
			<column name="VL_DOC" type="decimal" />
		</table>
		<table id="C170" description="Itens" parent="C100">
			<column name="NUM_ITEM"/>
			<column name="COD_ITEM"/>
			<column name="QTD" type="decimal"/>
			<column name="UNID"/>
			<column name="VL_ITEM" type="decimal" />
			<column name="CFOP"/>
			<column name="CST_ICMS"/>
			<column name="VL_BC_ICMS" type="decimal" />
			<column name="ALIQ_ICMS" type="decimal" />
			<column name="VL_ICMS" type="decimal" />
			<column name="VL_BC_ICMS_ST" type="decimal" />
			<column name="ALIQ_ST" type="decimal" />
			<column name="VL_ICMS_ST" type="decimal" />
			<column name="VL_IPI" type="decimal" />
		</table>		
	</tables-list>
    </hierarquical-schema>
"

## Requisitos

- xsdata
- spedpy
- pandas

## Como instalar

    $ pip install spedpyutils