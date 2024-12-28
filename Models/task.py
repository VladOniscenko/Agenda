from datetime import datetime

class Task:
    __name: str
    __description: str
    __priority: str
    __date: datetime
    __status: str
    __status: tuple[str]
    __STATUSES: tuple[str, ...] = ("Pending", "In Progress", "Completed", "On Hold", "Cancelled")
    __PRIORITIES: tuple[str, ...] = ('Low', 'Medium', 'High', 'Critical')
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

    @classmethod
    def statuses(cls):
        return cls.__STATUSES

    @classmethod
    def priorities(cls):
        return cls.__PRIORITIES

    @property
    def status_color(self):
        colors = {
            "Pending": ("rgba(255, 255, 255, 0.1)", "#5D4037"),
            "Completed": ("rgba(200, 230, 201, 0.3)", "#2C6B2F"),
            "Cancelled": ("rgba(255, 205, 210, 0.3)", "#9A1F1F"),
        }
        return colors.get(self.__status, ("rgba(255, 255, 255, 0.1)", "#5D4037"))

    def set_status(self, status: str):
        if status in self.__STATUSES:
            self.__status = status
        else:
            raise ValueError("Unexpected status")