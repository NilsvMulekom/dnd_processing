from dataclasses import dataclass

@dataclass
class raw_file:
    name: str
    body: list[str]