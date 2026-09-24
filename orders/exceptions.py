class OrderError(Exception):
    pass


class ValidationError(OrderError):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


class StorageError(OrderError):
    pass


class StorageNotFoundError(StorageError):
    pass


class StorageCorruptedError(StorageError):
    pass
