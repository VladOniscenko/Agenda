class User:
    id: None
    first_name: str
    last_name: str

    def __init__(self, first_name: str, last_name: str, identifier: int = None):
        self.id = identifier
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
