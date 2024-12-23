from os import fstat, path, remove

from fastapi import Form, UploadFile

from files.settings import settings


def file_size(file: UploadFile) -> int:
    return fstat(file.file.fileno()).st_size


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls