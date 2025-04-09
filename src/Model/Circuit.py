class Circuit:
    def __init__(self, name, location, country, **kwargs):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(location, str):
            raise TypeError("location must be a string")
        if not isinstance(country, str):
            raise TypeError("country must be a string")
        self.name = name
        self.location = location
        self.country = country
        self.additional_info = kwargs # Latitude and longitude for example

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
            f"Location: {self.location}\n"
            f"Country: {self.country}\n"
            f"{additional_info_str}"
        )
