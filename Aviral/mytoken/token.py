# token/token.py
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    literal: str
