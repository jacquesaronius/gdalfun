from abc import ABCMeta, abstractmethod

class IMapper:

    __metaclass__ = ABCMeta

    @abstractmethod
    def map(json_object) -> dict:
        raise NotImplementedError
