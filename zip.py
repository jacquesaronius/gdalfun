from zipfile import ZipFile
from uuid import uuid1
from abc import ABCMeta, abstractmethod

class IZip:
    __metaclass__ = ABCMeta

    @abstractmethod
    def extract(self) -> str:
        raise NotImplementedError

class Zip(IZip):
    def __init__(self, zip_file, guid = None, folder = "/tmp") -> None:
        self.zip_file = zip_file
        if guid is None:
            guid = uuid1()
        self.extraction_path = f"{folder}/{guid}"

    def extract(self) -> str:
        zf = ZipFile(self.zip_file)
        zf.extractall(self.extraction_path)
        return self.extraction_path

class ZipFactory:
    def create(zip_file) -> IZip:
        zip: IZip = Zip(zip_file)
        return zip


