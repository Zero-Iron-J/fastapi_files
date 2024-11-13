from pydantic import BaseModel


class Market(BaseModel):
    name : str
    call_num : str
    menu : dict[str,int]
    location : str


