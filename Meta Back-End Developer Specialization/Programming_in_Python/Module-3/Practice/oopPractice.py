class House :
    num_rooms = 5
    bathrooms = 2
    def cost_eval(self) :
        print(self.num_rooms)
        pass

house = House()
house.num_rooms=7
print(house.num_rooms)
print(House.num_rooms)

House.num_rooms=8
print(house.num_rooms)
print(House.num_rooms)