"""
3.    Create a class called Pet with attributes name and age. 
Implement a method within the class to calculate the age of the pet in equivalent human years. 
Additionally, create a class variable called species to store the species of the pet. 
Implement a method within the class that takes the species of the pet as input and 
returns the average lifespan for that species.

- Instantiate three objects of the Pet class with different names, ages, and species.
- Calculate and print the age of each pet in human years.
- Use the average lifespan function to retrieve and print the average lifespan for each pet's species.

ChatGPT history: https://chatgpt.com/share/68ac9700-f200-8010-befe-d90a297704de

"""

# Pet class to get pet age in human years
class Pet:

    # Allowed species
    species = {
        "dog", "cat", "rabbit", "hamster", "mouse", "rat",
        "bird", "goldfish", "betta", "gecko", "turtle", "tortoise", "horse"
    }
    # Dictionary to store the average lifespan of each type of pet
    __AVERAGE_LIFESPAN = {
        "dog": 12,
        "cat": 15,
        "rabbit": 10,
        "hamster": 2.5,
        "mouse": 2,
        "rat": 2.5,
        "bird": 8,
        "goldfish": 13,
        "betta": 3,
        "gecko": 17,
        "turtle": 30,
        "tortoise": 80,
        "horse": 28
        }

    def __init__(self, name : str, age : float, species : str):
        self.name = name
        self.__species = species.lower()
        self.age = max(age, 0)
        if species not in Pet.species:        # Chatgpt suggestion
            raise ValueError(f"Unsupported species: {self._species}")

    # Get the species, which I decided to make a private variable
    @property            # ChatGPT suggestion over just calling it a getter
    def species_type(self) -> str:
        return self.__species
    
    # Set the species, which I decided to make a private variable
    @species_type.setter
    def species_type(self, species : str) -> None:
        self.__species = species

    # Get the average lifespan depending on the pet's specifies
    @classmethod        # ChatGPT suggestion to make this a calass method
    def lifespan(cls, species : str) -> int:
        return cls.__AVERAGE_LIFESPAN.get(species, "Unknown")

    # Calculate the pet's age in human years. These calculations were based on ChatGPT
    def human_age(self) -> float:
        if self.__species == "dog":
            return self.__split_age(15.0, 9.0, 5.5)
        elif self.__species == "cat":
            return self.__split_age(15.0, 9.0, 4.0)
        elif self.__species == "rabbit":
            return self.__split_age(12.0, 8.0, 4.5)
        elif self.__species == "hamster":
            return self.age*2.5
        elif self.__species == "rat":
            return self.__rat_age()
        elif self.__species == "mouse":
            return self.__mouse_age()
        elif self.__species == "goldfish":
            return self.age*6.0
        elif self.__species == "betta":
            return self.age*20
        elif self.__species == "bird":
            return self.__split_age(12.0, 7.0, 7.0)
        elif self.__species == "gecko":
            return self.__split_age(12.0, 4.5, 4.5)
        elif self.__species == "horse":
            return self.__horse_age()
        elif self.__species == "turtle" or self.species == "tortoise":
            if self.age < 15:
                return 4.0*self.age
            return 4.0*15 + (self.age - 15) *2

        return self.age

    # Helper function as many pets have 3 distinct life phases. This is based on ChatGPT
    def __split_age(self, year1, year2, remainder):
        if self.age <= 0:
            return 0.0
        if self.age < 1:
            # linear within first year
            return year1 * self.age
        if self.age < 2:
            return year1 + (self.age - 1.0) * year2
        return year1 + year2 + (self.age - 2.0) * remainder

    # Rats have an age defined in months
    def __rat_age(self):
        months = self.age * 12
        if months < 6:
            return months *3 
        elif months < 12:
            return 18+(months - 6)*2
        return 30 + (months - 12.0) *2.5

    # Mice have an age defined in months
    def __mouse_age(self):
        months = self.age * 12
        if months < 6:
            return months * (20.0/6.0) 
        elif months < 24:
            return 20+(months - 6)* (60.0/18.0)
        return 80 + (months - 24.0) *(60.0/18.0)

    # Horses have 4 stages isntead of 3
    def __horse_age(self):
        if self.age < 1:
            return 6.5 *self.age
        if self.age < 2:
            return 6.5 + (self.age - 1.0) * (13.0 - 6.5)
        if self.age < 3:
            return 13.0 + (self.age - 2.0) * (18.0 - 13.0)
        if self.age < 4:
            return 18.0 + (self.age - 3.0) * (20.5 - 18.0)
        if self.age < 5:
            return 20.5 + (self.age - 4.0) * 2.5
        return 23.0 + (self.age - 5.0) * 2.5

# Initial pet list of 3 pets
pet_list = [Pet("Fluffy", 5.5, "cat"), Pet("Rover", 3.1, "dog"), Pet("Moonlight", 2.2, "betta")]

# Print the age of each pet in human years
print("Age in Human Years")
for p in pet_list:
    print(p.name + ":", p.human_age())

# Print the average lifespance of each pet 
print("\nAverage Lifespan in Years")
for p in pet_list:
    print(f"{p.name}, {p.species_type}: {Pet.lifespan(p.species_type)}")



 