from typing import List
from schemas import Listing

STORE: List[Listing] = []
_id = 1

def next_id():
    global _id
    v = _id
    _id += 1
    return v
