class FarmAnimals:
    age = 0  # days
    weight = 0  # kg

    def __init__(self, age, weight):
        self.age = age
        self.weight = weight

    def feeding(self):
        print('Ням-Ням!!!')

    def growing_up(self, days):
        self.age += days


class Birds:

    def laying_eggs(self):
        pass

    def flight(self):
        pass


class Cow(FarmAnimals):
    average_milk = 3  # litres

    def __init__(self, age, weight, average_milk):
        self.average_milk = average_milk
        super().__init__(age, weight)

    def milking(self):
        pass


class Goat(FarmAnimals):
    average_wool = 1  # kg
    average_milk = 1  # litres

    def __init__(self, age, weight, average_wool, average_milk):
        self.average_wool = average_wool
        self.average_milk = average_milk
        super().__init__(age, weight)

    def cutting(self):
        pass

    def milking(self):
        pass


class Sheep(FarmAnimals):
    average_wool = 2  # kg

    def __init__(self, age, weight, average_wool):
        self.average_wool = average_wool
        super().__init__(age, weight)

    def cutting(self):
        pass


class Pig(FarmAnimals):
    average_meet = 20  # kg

    def __init__(self, age, weight, average_meet):
        self.average_meet = average_meet
        super().__init__(age, weight)


class Duck(FarmAnimals, Birds):
    average_eggs = 5  # pieces per month
    average_meet = 3  # kg

    def __init__(self, age, weight, average_eggs, average_meet):
        self.average_eggs = average_eggs
        self.average_meet = average_meet
        super().__init__(age, weight)


class Chicken(FarmAnimals, Birds):
    average_eggs = 10  # pieces per month
    average_meet = 3  # kg

    def __init__(self, age, weight, average_eggs, average_meet):
        self.average_eggs = average_eggs
        self.average_meet = average_meet
        super().__init__(age, weight)


class Goose(FarmAnimals, Birds):
    average_eggs = 7  # pieces per month
    average_meet = 10  # kg

    def __init__(self, age, weight, average_eggs, average_meet):
        self.average_eggs = average_eggs
        self.average_meet = average_meet
        super().__init__(age, weight)
