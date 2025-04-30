class Race:
    def __init__(self, year, name, date, **kwargs):
        if not isinstance(name, str):
            raise TypeError("name doit être de type string")
        if not isinstance(year, int):
            raise TypeError("year doit être de type string")
        if not isinstance(date, str):
            raise TypeError("date doit être de type string")
        self.name = name
        self.year = year
        self.date = date
        self.additional_info = kwargs

    def __str__(self):
        additional_info_str = (
            "\n".join([f"{key}: {value}" for key, value in self.additional_info.items()])
            if self.additional_info
            else "No additional info"
        )

        return f"Name: {self.name}\n" f"Date: {self.date}\n" f"{additional_info_str}"
