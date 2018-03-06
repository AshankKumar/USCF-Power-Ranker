class Player:

    def __init__(self):
        self.idNum = ""
        self.name = ""
        self.rating = 0

    def __init__(self, idNum, n, r):
        self.idNum = idNum
        self.name = n
        self.rating = r

    def get_idNum(self):
        return self.idNum

    def get_name(self):
        return self.name

    def get_rating(self):
        return self.rating

    def __repr__(self):
        return self.idNum + ", " + self.name + ", " + str (self.rating)

    def set_rating(self, r):
        self.rating = r
