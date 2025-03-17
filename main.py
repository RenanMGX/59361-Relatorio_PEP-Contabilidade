from Entities.extrair_dados_sap import ExtrairDadosSAP
from Entities.dependencies.arguments import Arguments
from Entities import utils
from datetime import datetime
from Entities.informativo import Informativo
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
    except KeyError as err:
        print(err)
        raise Exception("Faltam argumentos no arquivo args.json")
    return args

class Execute:
    @staticmethod
    def start():
        Informativo.limpar()
        Informativo.register("Iniciando a extração de dados do SAP", color='<django:green>')
        argumentos:dict = carregar_json()
        Informativo.register(f"Argumentos carregados", color='<django:green>')
        
        ExtrairDadosSAP().limpar_pasta_download()

        lista_arquivos_projetos = []
        for divisao in argumentos['divisao']:
            NUM_TENTATIVAS = 3
            for _ in range(1, (NUM_TENTATIVAS +1)):
                sap = ExtrairDadosSAP()
                try:
                    Informativo.register(f"Extraindo dados da divisão {divisao}", color='<django:blue>')
                    lista_arquivos_projetos.append(sap.ExtrairDados(divisao=divisao[0:4], date=argumentos['date'], acumulado=argumentos['acumulado'], final_date=argumentos['final_date']))
                    Informativo.register(f"    Extração da divisão {divisao} finalizada", color='<django:green>')
                    sap.fechar_sap()
                    del sap
                    break
                except Exception as e:
                    Informativo.register(f"    {_}/{NUM_TENTATIVAS} - Erro ao extrair dados da divisão {divisao}: {type(e), e}", color='<django:yellow>', register_log=True)
                    print(type(e), e)
                sap.fechar_sap()
                del sap
                if _ == NUM_TENTATIVAS:
                    Informativo.register(f"    {_}/{NUM_TENTATIVAS} - Não foi possivel extrair o relarotio {divisao}", color='<django:red>', register_log=True)
        
        Informativo.register("Extração de dados finalizada", color='<django:green>')
        
        if lista_arquivos_projetos:
            zip_path = os.path.join(os.getcwd(), "fileZip")
            if not os.path.exists(zip_path):
                os.makedirs(zip_path)
            for file in os.listdir(zip_path):
                os.remove(os.path.join(zip_path, file))
                
            utils.zipar_dados_da_pasta(lista_arquivos_projetos, zip_name=os.path.join(zip_path, datetime.now().strftime("%Y%m%d%H%M%S_projetosPEP.zip")))
        
        Informativo.register("Arquivo Zip Criado", color='<django:green>')
        
        #print(lista_arquivos_projetos)
        #import pdb;pdb.set_trace()
        #sap.fechar_sap()
        Informativo.register("Finalizado!", color='<django:green>')
        
        
if __name__ == "__main__":
    Arguments({
        "start": Execute.start
    })
    