class Address:
    def __init__(self, line_one, line_two, city, postcode):
        self._line_one = line_one
        self._line_two = line_two
        self._city = city
        self._postcode = postcode

    @property
    def line_one(self):
        return self._line_one

    @property
    def line_two(self):
        return self._line_two

    @property
    def city(self):
        return self._city

    @property
    def postcode(self):
        return self._postcode

    