
import shutil
from uuid import uuid1
from abc import ABCMeta, abstractmethod

class DBCopier:
    
    __metaclass__: ABCMeta
    
    @abstractmethod
    def copy(source):
        raise NotImplementedError

class SQLiteCopier:

    def copy(source: str) -> str:
        dst = f"/tmp/{uuid1()}.db"
        shutil.copy(source, dst)
        return dst
