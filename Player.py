class Player:

    def __init__(self):
        self.name = ""
        self.rating = 0

    def __init__(self, n, r):
        self.name = n
        self.rating = r

    def get_name(self):
        return self.name

    def get_rating(self):
        return self.rating

    def __repr__(self):
        return self.name + ", " + str (self.rating)

    def set_rating(self, r):
        self.rating = r


