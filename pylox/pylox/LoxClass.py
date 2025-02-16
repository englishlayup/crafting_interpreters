from typing import Final


class LoxClass:
    def __init__(self, name: str) -> None:
        self.name: Final[str] = name

    def __str__(self) -> str:
        return self.name
