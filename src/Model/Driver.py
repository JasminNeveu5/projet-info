class Driver:
    def __init__(self, id:int, forename: str, surname:str, nationality:str,**kwargs):
        if not isinstance(id, int):
            raise TypeError("id doit être de type int")
        if not isinstance(forename, str):
            raise TypeError("forename doit être de type str")
        if not isinstance(surname, str):
            raise TypeError("surname doit être de type str")
        if not isinstance(nationality, str):
            raise TypeError("nationality doit être de type str")

        self.id = id
        self.forename = forename
        self.surname = surname
        self.nationality = nationality
        self.additional_info = kwargs

    def __str__(self):
        return (f"Forename: {self.forename} \nSurname: {self.surname}"
                f"\nNationality: {self.nationality} \n{self.additional_info}")
