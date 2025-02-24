import os
import json
from datetime import datetime
from typing import Literal

class Informativo:
    path = os.path.join(os.getcwd(), "informativo.json")
    
    @staticmethod
    def load() -> list:
        if not os.path.exists(Informativo.path):
            with open(Informativo.path, 'w') as f:
                json.dump([], f)
        with open(Informativo.path, 'r') as f:
            return json.load(f)
        
    @staticmethod
    def register(text:str, color:Literal["", "<django:red>", "<django:yellow>", "<django:green>", "<django:blue>"]= "") -> None:
        data = Informativo.load()
        text = datetime.now().strftime(f"[%d/%m/%Y %H:%M:%S] - {text} {color}")
        data.append(text)
        with open(Informativo.path, 'w') as f:
            json.dump(data, f)
        print(text)
        
    @staticmethod
    def limpar() -> None:
        with open(Informativo.path, 'w') as f:
            json.dump([], f)
        
if __name__ == "__main__":
    Informativo.limpar()
    Informativo.register("Hello", color='<django:green>')
    Informativo.register("World!", color='<django:green>')
    