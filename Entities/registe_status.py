import json
import os
from datetime import datetime
from typing import Literal

def valid_status_path():
    path = os.path.join(os.getcwd(), 'mp_status')
    if not os.path.exists(path):
        os.mkdir(path)
    return os.path.join(path, datetime.now().strftime("status_%Y%m%d%H%M%S_.txt"))

class RegisterStatus:
    @property
    def path(self):
        return self.__path
    
    def __init__(self, path) -> None:
        self.__path = path
                  
    def delete(self):
        if os.path.exists(self.path):
            try:
                os.unlink(self.path)
            except:
                pass
        
    def read(self) -> dict:
        with open(self.path, 'r', encoding='utf-8') as _file:
            return json.load(_file)
    
    def register(self, status:Literal['running', 'stopped', 'created']):
        with open(self.path, 'w', encoding="utf-8") as _file:
            json.dump({
                'status': status,
                'date' : datetime.now().isoformat()
            }, _file)

if __name__ == "__main__":
    from time import sleep
    reg = RegisterStatus(valid_status_path())
    print(reg.read())
    sleep(1)
    print(reg.read())
    reg.register('running')
    sleep(1)
    print(reg.read())
    sleep(1)
    print(reg.read())
    reg.register('stopped')
    sleep(1)
    print(reg.read())
    sleep(1)







