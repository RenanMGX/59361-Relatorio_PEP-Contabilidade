from dependencies.sap import SAPManipulation
from dependencies.config import Config
from dependencies.credenciais import Credential
from dependencies.functions import Functions
from datetime import datetime
from time import sleep
import os
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')



class ExtrairDadosSAP(SAPManipulation):
    @property
    def download_path(self):
        return self.__download_path
    
    def __init__(self, download_path:str=os.path.join(os.getcwd(), "Downloads")):
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        self.__download_path:str = download_path
        
        crd:dict = Credential(Config()['credenciais']['sap']).load()
        super().__init__(user=crd['user'], password=crd['password'], ambiente=crd['ambiente'], new_conection=True)
        
    
    @SAPManipulation.start_SAP
    def test(self):
        import pdb;pdb.set_trace()
    
    def limpar_pasta_download(self):
        for file in os.listdir(self.__download_path):
            os.remove(os.path.join(self.__download_path, file))    
        
    @SAPManipulation.start_SAP
    def ExtrairDados(self, *, centro:str, date:datetime, acumulado:bool, final_date:datetime|None=None):
        if final_date:
            if final_date < date:
                final_date = None
        if not acumulado:
            final_date = None
        
        self.session.findById("wnd[0]/tbar[0]/okcd").text = "/n zps101"
        self.session.findById("wnd[0]").sendVKey(0)
        
        try:
            self.session.findById("wnd[1]/usr/ctxtTCNT-PROF_DB").text = "ZPS000000001"
            self.session.findById("wnd[1]/tbar[0]/btn[0]").press()
        except:
            pass
        
        self.session.findById("wnd[0]/usr/ctxtCN_PROJN-LOW").text = centro
        self.session.findById("wnd[0]/usr/ctxt$6-KOKRS").text = "GPN"
        self.session.findById("wnd[0]/usr/txt$ZAF").text = str(date.year)
        self.session.findById("wnd[0]/usr/ctxt$ZPI").text = str(date.month)
        self.session.findById("wnd[0]/usr/ctxt$ZPF").text = str(final_date.month) if final_date else str(date.month)
        self.session.findById("wnd[0]/tbar[1]/btn[8]").press()
        
        sleep(2)
        
        #import pdb;pdb.set_trace()
        
        #cont = 1
        for cont in range(1, 1000):
            numberNode = str(cont).zfill(6)
            text = self.session.findById("wnd[0]/shellcont/shell/shellcont[2]/shell").GetNodeTextByKey(numberNode)
            
            # if text:
            #     print(f'{text} == PEP {centro.upper()}.P  ==> ', (text == f"PEP {centro.upper()}.P"))
            if text == f"PEP {centro.upper()}.P":
                break

            if cont >= 999:
                raise Exception(f"Não foi encontrado o PEP {centro}.P!")
            
            #cont += 1
            
        self.session.findById("wnd[0]/shellcont/shell/shellcont[2]/shell").selectedNode = numberNode #type: ignore
        
        if acumulado:
            campo = self.session.findById("wnd[0]/usr/lbl[76,19]")
        else:
            for num in range(1, 50):
                sleep(.25)
                try:
                    campo = self.session.findById("wnd[0]/usr/lbl[106,19]")
                    break
                except:
                    self.session.findById("wnd[0]/usr").horizontalScrollbar.position = num
                    
                if num >= 49:
                    raise Exception("Não foi encontrado o campo de acumulado!")
            
        value = campo.text #type: ignore
        
        campo.setFocus() #type: ignore
        
        # import pdb; pdb.set_trace()
        # return
        
        self.session.findById("wnd[0]").sendVKey(2)
        
        self.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell/shellcont[1]/shell").contextMenu()
        self.session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell/shellcont[1]/shell").selectContextMenuItem("&XXL")
        
        self.session.findById("wnd[1]/tbar[0]/btn[0]").press()
        
        file_path = os.path.join(self.__download_path, date.strftime(f"{centro.upper()}_%Y_%B{((final_date.strftime("_a_%B")) if final_date else "")}_relatoriosPEP.xlsx"))
        if os.path.exists(file_path):
            Functions.fechar_excel(file_path)
            os.remove(file_path)
        
        self.session.findById("wnd[1]/usr/ctxtDY_PATH").text = os.path.dirname(file_path)
        self.session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = os.path.basename(file_path)

        self.session.findById("wnd[1]/tbar[0]/btn[0]").press()
        
        sleep(5)
        
        Functions.fechar_excel(file_path)
        
        #import pdb;pdb.set_trace()
        
        return file_path
