from datetime import datetime

class Task:
    __name: str
    __description: str
    __priority: str
    __date: datetime
    __status: str
    __status: tuple[str]
    __STATUSES: tuple[str, ...] = ("Pending", "In Progress", "Completed", "On Hold", "Cancelled")
    __READABLE: tuple[str, ...] = ('id', 'name', 'description', 'priority', 'date', 'status')

    def __init__(self, name: str, description: str, date: datetime = datetime.now(), priority: str = 1, status: str = "Pending", identifier: int = None):
        self.__id = identifier
        self.__name = name
        self.__description = description
        self.__priority = priority
        self.__date = date
        self.__status = status

    # return private attributes
    def __getattr__(self, attr):
        protected = f"_{self.__class__.__name__}__{attr}"

        # check if attr isset and not in
        if attr in self.__READABLE and protected in self.__dict__:
            return self.__dict__[protected]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    # represent instance
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!r}" for key, value in self.__dict__.items()]))
