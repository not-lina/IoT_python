import faker
import random
from dataclasses import dataclass

@dataclass
class UserModel():
    firstname: str
    lastname: str
    age: int
    gender: str
    username: str
    address: str
    email: str

    def toJson(self):
        return self.__dict__

    def toCsv(self):
        return [self.__dict__[key] for key in self.__dict__.keys()]

    def headers(self):
        return [key for key in self.__dict__.keys()]

    def __repr__(self):
        return self.toJson()


class UserFactory(UserModel):
    def __init__(self):
        F = faker.Faker()
        gender = 'M' if random.random() > .5 else 'F'
        firstname = F.first_name_male() if gender == "M" else F.first_name_female()

        super().__init__(
            firstname,
            F.last_name(),
            F.random_int(min=18, max=90),
            gender,
            F.user_name(),
            F.address(),
            F.email()
        )

    def toJson(self):
        dc = super().toJson()
        return dc

    def toCsv(self):
        dc = super().toCsv()
        return dc

    def headers(self):
        return super().headers()

    def __repr__(self):
        return self.toJson()
