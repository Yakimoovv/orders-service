from pathlib import Path
from types import TracebackType
from typing import TextIO


class AtomicWriter:
    def __init__(
        self, path: Path, encoding: str = "utf-8", newline: str | None = None
    ) -> None:
        self.path = path
        self.encoding = encoding
        self.newline = newline
        self.tmp = path.with_name(path.name + ".tmp")

    def __enter__(self) -> TextIO:
        self.file = open(self.tmp, "w", encoding=self.encoding, newline=self.newline)
        return self.file

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.file.close()
        if exc_type is None:
            self.tmp.replace(self.path)
        else:
            self.tmp.unlink(missing_ok=True)
