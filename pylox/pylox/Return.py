
from typing import Final


class Return(RuntimeError):
    def __init__(self, value: object) -> None:
        super().__init__()
        self.value: Final[object] = value
