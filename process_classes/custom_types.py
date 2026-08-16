from dataclasses import dataclass

@dataclass
class TextFile:
    name: str
    body: list[str]