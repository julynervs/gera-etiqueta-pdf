# %%
import os
import glob
from zipfile import ZipFile
from time import sleep

print("Coloque o ZIP da etiqueta na pasta")
sleep(1)

def imprimir_etiqueta(arquivo_pdf):
    try:
        os.startfile(os.path.abspath(arquivo_pdf), "print")
        print(f"Imprimindo {arquivo_pdf}")
        # print(f"{os.path.abspath(arquivo_pdf)}")
    except OSError:
        print("Falha na impressão da etiqueta. Defina um leitor padrão para o PDF e tente novamente.")
    else:
        print("Etiqueta impressa com sucesso!\n")
        os.remove(arquivo_pdf)

def converter_zpl_para_pdf():
    # faz a leitura do txt extraido do zip
    zpl_open = open(f"{nome_zip}/Etiqueta de envio.txt", 'r')
    zpl = zpl_open.read()
      
    ## script de conversão do código ZPL da etiqueta para PDF ##
    # adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
    url = "http://api.labelary.com/v1/printers/8dpmm/labels/4x6/"
    files = {"file": zpl}
    headers = {"Accept": "application/pdf"}  # omit this line to get PNG images back
    response = requests.post(url, headers=headers, files=files, stream=True)
    # verifica se a requisicão deu certo
    if response.status_code == 200:
        response.raw.decode_content = True
        with open(f"{nome_zip}.pdf", "wb") as out_file:  # change file name for PNG images
            shutil.copyfileobj(response.raw, out_file)
            zpl_open.close()
            out_file.close()
            sleep(1)
            print("PDF gerado!\n")
    else:
        print("Falha na conversão para PDF")
        print("Error: " + response.text)

def extrair_arquivo():
    try:
        # cria um objeto ZipFile para extrair os arquivos de dentro do zip
        with ZipFile(arquivo_zip, 'r') as zip:
            zip.extractall(nome_zip)
            print("Extraindo txt")
            sleep(1)
    # verifica se a extração deu certo
    except Exception:
        print("Falha na extraçao")
    else:
        converter_zpl_para_pdf()

while True:
    # procura todos o arquivos com o final .zip da pasta atual
    lista_zips = glob.glob("**/*.zip", recursive=True)  

    from time import sleep
    import requests
    import shutil

    # percorre lista que o glob retorna
    for arquivo_zip in lista_zips:
        if "Etiqueta MercadoEnvios" in str(arquivo_zip):
            nome_zip = str(arquivo_zip).replace(".zip","")
            print(f"{nome_zip} encontrado")

            extrair_arquivo()
            shutil.rmtree(nome_zip)
            os.remove(arquivo_zip)     
        else:
            # remove o zip e a pasta descompactada
            shutil.rmtree(nome_zip)
            os.remove(arquivo_zip)
    
    # procura os pdfs da pasta 
    lista_pdfs = glob.glob("**/*.pdf", recursive=True)
    for arquivo_pdf in lista_pdfs:
        if "Etiqueta MercadoEnvios" in str(arquivo_pdf):
            imprimir_etiqueta(arquivo_pdf)
            sleep(5)

            
