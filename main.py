from Entities.extrair_dados_sap import ExtrairDadosSAP
from Entities.dependencies.arguments import Arguments
from Entities import utils
from datetime import datetime
import os
import json

def carregar_json(*, path:str=os.path.join(os.getcwd(), "args.json"), delete_file:bool=True) -> dict:
    args:dict = {}
    if os.path.exists(path):
        with open(path) as f:
            args = json.load(f)
        if delete_file:
            os.remove(path)
    else:
        raise Exception("Arquivo args.json não encontrado")
    try:
        if not isinstance(args['divisao'], list):
            raise Exception("Divisão deve ser uma lista")            
        args['date'] = datetime.fromisoformat(args['date'])
        args['acumulado']
        if args['final_date']:
            args['final_date'] = datetime.fromisoformat(args['final_date'])
    except KeyError:
        raise Exception("Faltam argumentos no arquivo config.json")
    return args

class Execute:
    @staticmethod
    def start():
        argumentos:dict = carregar_json(delete_file=False)
        
        sap = ExtrairDadosSAP()
        sap.limpar_pasta_download()
        
        lista_arquivos_projetos = []
        for divisao in argumentos['divisao']:
            try:
                lista_arquivos_projetos.append(sap.ExtrairDados(divisao=divisao[0:4], date=argumentos['date'], acumulado=argumentos['acumulado'], final_date=argumentos['final_date']))
            except Exception as e:
                print(type(e), e)
        
        if lista_arquivos_projetos:
            zip_path = os.path.join(os.getcwd(), "fileZip")
            if not os.path.exists(zip_path):
                os.makedirs(zip_path)
            for file in os.listdir(zip_path):
                os.remove(os.path.join(zip_path, file))
                
            utils.zipar_dados_da_pasta(lista_arquivos_projetos, zip_name=os.path.join(zip_path, datetime.now().strftime("%Y%m%d%H%M%S_projetosPEP.zip")))
        
        print(lista_arquivos_projetos)
        #import pdb;pdb.set_trace()
        sap.fechar_sap()
        
        
if __name__ == "__main__":
    #print(carregar_json(delete_file=False))
    
    Arguments({
        "start": Execute.start
    })
    