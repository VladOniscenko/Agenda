from datetime import datetime, timedelta


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
            "Pending": ("rgba(63, 63, 63, 0.8)", "lightgray"),  # Dark gray background, light gray text
            "Completed": ("rgba(46, 77, 46, 0.8)", "lightgreen"),  # Dark green background, light green text
            "Cancelled": ("rgba(77, 46, 46, 0.8)", "lightcoral"),  # Dark red background, light coral text
            "In Progress": ("rgba(77, 63, 46, 0.8)", "wheat"),  # Warm brown background, wheat-colored text
            "On Hold": ("rgba(46, 59, 77, 0.8)", "lightskyblue"),  # Dark blue-gray background, sky blue text
        }

        return colors.get(self.__status, ("rgba(255, 255, 255, 0.1)", "white"))

    @property
    def priority_color(self):
        colors = {
            "Low": ("rgba(255, 255, 255, 0.1)", "white"),  # Low priority: Light background, white text
            "Medium": ("rgba(46, 59, 77, 0.8)", "lightskyblue"),  # Medium priority: Darker blue-gray, light blue text
            "High": ("rgba(255, 165, 0, 0.3)", "rgba(204, 102, 0, 0.8)"),  # High priority: Orange background, darker orange text
            "Critical": ("rgba(77, 46, 46, 0.8)", "lightcoral"),  # Critical priority: Dark red background, light coral text
        }

        # Ensure only valid priorities are used; fallback for invalid priority
        return colors.get(self.__priority,("rgba(255, 255, 255, 0.1)", "white"))

    def set_status(self, status: str):
        if status in self.__STATUSES:
            self.__status = status
        else:
            raise ValueError("Unexpected status")

    @property
    def task_time_label(self):
        current_date = datetime.now()
        task_date = self.get_datetime()

        # Compare the task date with the current date
        if task_date.date() == current_date.date():
            time_label_text = 'Today'
        elif task_date.date() == (current_date + timedelta(days=1)).date():
            time_label_text = 'Tomorrow'
        elif task_date.date() < current_date.date():
            time_label_text = 'Passed'
        else:
            time_label_text = task_date.strftime('%d-%m-%Y')

        return time_label_text

    def get_datetime(self):
        # Convert task.date string to QDateTime
        try:
            return datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            return datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")