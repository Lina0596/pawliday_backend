from abc import ABC, abstractmethod


class AbstractDataHandler(ABC):


    @abstractmethod
    def get_user_dogs(self, user_id):
        """
        """
        pass


    @abstractmethod
    def get_user_dogs_today(self, user_id):
        """
        """
        pass
        

    @abstractmethod
    def get_dog(self, dog_id):
        """
        """
        pass


    @abstractmethod
    def add_dog(self, user_id):
        """
        """
        pass


    @abstractmethod
    def update_dog(self, dog_id):
        """
        """
        pass


    @abstractmethod
    def delete_dog(dog_id):
        """
        """
        pass


    @abstractmethod
    def add_user():
        """
        """
        pass
