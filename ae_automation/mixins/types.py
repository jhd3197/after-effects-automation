from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, FilePath, HttpUrl, ValidationError, validator

class ae_files(BaseModel):
    id: int
    name: str
    type: str

class ae_bot(BaseModel):
    projectName: str
    files: List[ae_files] = []