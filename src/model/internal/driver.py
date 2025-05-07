class Driver:
    def __init__(self, forename: str, surname: str, nationality: str, **kwargs):
        if not isinstance(forename, str):
            raise TypeError("forename doit être de type str")
        if not isinstance(surname, str):
            raise TypeError("surname doit être de type str")
        if not isinstance(nationality, str):
            raise TypeError("nationality doit être de type str")

        self.forename = forename
        self.surname = surname
        self.nationality = nationality
        self.additional_info = kwargs

    def __str__(self):
        additional_info_str = (
            "\n".join(
                [f"{key}: {value}" for key, value in self.additional_info.items()]
            )
            if self.additional_info
            else "No additional info"
        )

        return (
            f"Forename: {self.forename}\n"
            f"Surname: {self.surname}\n"
            f"Nationality: {self.nationality}\n"
            f"{additional_info_str}"
        )

    def __eq__(self, other_driver):
        return (self.forename == other_driver.forename) & (self.surname == other_driver.surname) & (self.nationality == other_driver.nationality)
