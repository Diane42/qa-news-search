from typing import Union


class BasicException(Exception):
    def __init__(self, code: int, detail: Union[str, None] = None):
        self.code = code
        self.detail = detail

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(error_code={self.code!r}, detail={self.detail!r})"


class ElasticsearchException(BasicException):
    pass
