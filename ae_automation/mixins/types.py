from pydantic import BaseModel


class ae_files(BaseModel):
    id: int
    name: str
    type: str


class ae_bot(BaseModel):
    projectName: str
    files: list[ae_files] = []
