
import shutil
from uuid import uuid1
from abc import ABCMeta, abstractclassmethod

class DBCopier:
    
    __metaclass__: ABCMeta
    
    @abstractclassmethod
    def copy(source):
        raise NotImplementedError

class SQLiteCopier(DBCopier):

    def copy(source: str) -> str:
        dst = f"/tmp/{uuid1()}.db"
        shutil.copy(source, dst)
        return dst
