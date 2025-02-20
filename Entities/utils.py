import os
import zipfile
from datetime import datetime            
            
def zipar_dados_da_pasta(list_files:list, *, zip_name:str=""):
    if zip_name == "":
        zip_name = datetime.now().strftime("%Y%m%d%H%M%S_relatoriosPEP.zip")
        zip_name = os.path.join(os.getcwd(), zip_name)
    elif not zip_name.lower().endswith(".zip"):
        zip_name += ".zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in list_files:
            if os.path.exists(file):
                zf.write(file, os.path.relpath(file,os.path.dirname(file)))
                
                
                
if __name__ == "__main__":
    pass
