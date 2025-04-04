from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from abstract_handler import AbstractDataHandler
from models import Base, Sitter, Owner, Dog, Stay, Trick, Knowledge


class SQLiteHandler(AbstractDataHandler):
    def __init__(self, db_file_name):
        self.engine = create_engine(f'sqlite:///data/{db_file_name}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)


    def get_user_dogs(self, user_id):
        """
        """
        pass


    def get_user_dogs_today(self, user_id):
        """
        """
        pass
        

    def get_dog(self, dog_id):
        """
        """
        pass


    def add_dog(self, user_id):
        """
        """
        pass


    def update_dog(self, dog_id):
        """
        """
        pass


    def delete_dog(dog_id):
        """
        """
        pass


    def add_user():
        """
        """
        pass


data_manager = SQLiteHandler('pawliday.db')