class Constructor:
    def __init__(self, name, nationality, **kwargs):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(nationality, str):
            raise TypeError("country must be a string")
        self.name = name
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
            f"Name: {self.name}\n"
            f"Country: {self.nationality}\n"
            f"{additional_info_str}"
        )
