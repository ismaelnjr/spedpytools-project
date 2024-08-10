import os

# Dicionário com os códigos dos estados
codigos_uf = {
    '11': ('RO', 'Rondônia'),
    '12': ('AC', 'Acre'),
    '13': ('AM', 'Amazonas'),
    '14': ('RR', 'Roraima'),
    '15': ('PA', 'Pará'),
    '16': ('AP', 'Amapá'),
    '17': ('TO', 'Tocantins'),
    '21': ('MA', 'Maranhão'),
    '22': ('PI', 'Piauí'),
    '23': ('CE', 'Ceará'),
    '24': ('RN', 'Rio Grande do Norte'),
    '25': ('PB', 'Paraíba'),
    '26': ('PE', 'Pernambuco'),
    '27': ('AL', 'Alagoas'),
    '28': ('SE', 'Sergipe'),
    '29': ('BA', 'Bahia'),
    '31': ('MG', 'Minas Gerais'),
    '32': ('ES', 'Espírito Santo'),
    '33': ('RJ', 'Rio de Janeiro'),
    '35': ('SP', 'São Paulo'),
    '41': ('PR', 'Paraná'),
    '42': ('SC', 'Santa Catarina'),
    '43': ('RS', 'Rio Grande do Sul'),
    '50': ('MS', 'Mato Grosso do Sul'),
    '51': ('MT', 'Mato Grosso'),
    '52': ('GO', 'Goiás'),
    '53': ('DF', 'Distrito Federal')
}

# Remove assinatura do arquivo sped se necessário
def rm_signature(filedir: str):

    # Lista todos os arquivos TXT na pasta
    arquivos_txt = [arquivo for arquivo in os.listdir(filedir) if arquivo.lower().endswith(".txt")]

    # Processa cada arquivo
    for arquivo in arquivos_txt:
        caminho_arquivo = os.path.join(filedir, arquivo)
        with open(caminho_arquivo, "r", encoding='utf-8') as arquivo_original:
            linhas = arquivo_original.readlines()

        i = 0
        for linha in linhas:
            if linha.startswith("|9999|"):
                break
            else:   
                i+=1
    
        # Remove a assinatura digital apos registro 9999
        linhas = linhas[:i]

        # Salva o conteúdo modificado em um novo arquivo
        novo_caminho_arquivo = os.path.join(filedir, f"modified_{arquivo}")
        with open(novo_caminho_arquivo, "w", encoding="utf-8") as novo_arquivo:
            novo_arquivo.writelines(linhas)