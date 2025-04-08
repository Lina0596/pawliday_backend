from abc import ABC, abstractmethod


class AbstractDataHandler(ABC):


    @abstractmethod
    def get_all_owners(self):
        """
        """
        pass

    
    @abstractmethod
    def add_owner(self, name, email, phone_number):
        """
        """
        pass


    @abstractmethod
    def update_owner(self, owner_id, name, email, phone_number):
        """
        """
        pass
    

    @abstractmethod
    def delete_owner(self, owner_id):
        """
        """
        pass


    @abstractmethod
    def add_dog(self, chip_id, owner_id, name, birth_date, breed, height, weight, food_per_day, gender, castrated, character, sociable, training, img_url):
        """
        """
        pass
    
    
    @abstractmethod
    def get_owner_dogs(self, owner_id):
        """
        """
        pass
        

    @abstractmethod
    def get_dog(self, dog_id):
        """
        """
        pass


    @abstractmethod
    def update_dog(self, dog_id, chip_id, owner_id, name, birth_date, breed, height, weight, food_per_day, gender, castrated, character, sociable, training, img_url):
        """
        """
        pass


    @abstractmethod
    def delete_dog(dog_id):
        """
        """
        pass
