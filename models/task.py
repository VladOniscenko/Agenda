from datetime import datetime

class Task:
    __name: str
    __description: str
    __priority: str
    __date: datetime
    __status: str
    __status: tuple[str]
    __STATUSES: tuple[str, ...] = ("Pending", "In Progress", "Completed", "On Hold", "Cancelled")

    def __init__(self, name: str, description: str, date: datetime = datetime.now(), priority: str = 1, status: str = "Pending"):
        self.__name = name
        self.__description = description
        self.__priority = priority
        self.__date = date
        self.__status = status
