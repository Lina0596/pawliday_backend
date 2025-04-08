from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from abstract_handler import AbstractDataHandler
from models import Base, Sitter, Owner, Dog, Stay, Trick, Knowledge
import json


class SQLiteHandler(AbstractDataHandler):
    def __init__(self, db_file_name):
        self.engine = create_engine(f'sqlite:///data/{db_file_name}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)


    def get_all_owners(self):
        """
        """
        with self.Session() as session:
            owners = session.query(Owner).all()
            return owners

    
    def add_owner(self, name, email, phone_number):
        """
        """
        with self.Session() as session:
            new_owner = Owner(
                sitter_id=1,
                name=name,
                email=email,
                phone_number=phone_number
            )
            session.add(new_owner)
            session.commit()


    def update_owner(self, owner_id, name, email, phone_number):
        """
        """
        with self.Session() as session:
            owner_to_update = session.query(Owner).filter(Owner.owner_id == owner_id).first()
            owner_to_update.name = name
            owner_to_update.email = email
            owner_to_update.phone_number = phone_number
            session.commit()


    def delete_owner(self, owner_id):
        """
        """
        with self.Session() as session:
            owner_to_delete = session.query(Owner).filter(Owner.owner_id == owner_id).first()
            session.delete(owner_to_delete)
            session.commit()


    def add_dog(self, chip_id, owner_id, name, birth_date, breed, height, weight, food_per_day, gender, castrated, character, sociable, training, img_url):
        """
        """
        with self.Session() as session:
            new_dog = Dog(
                chip_id=chip_id,
                owner_id=owner_id,
                name=name,
                birth_date=birth_date,
                breed=breed,
                height=height,
                weight=weight,
                food_per_day=food_per_day,
                gender=gender,
                castrated=castrated,
                character=character,
                sociable=sociable,
                training=training,
                img_url=img_url
            )
            session.add(new_dog)
            session.commit()
    
    
    def get_owner_dogs(self, owner_id):
        """
        """
        with self.Session() as session:
            owner_dogs = session.query(Dog).filter(Dog.owner_id == owner_id).all()
            return owner_dogs
        

    def get_dog(self, dog_id):
        """
        """
        with self.Session() as session:
            dog = session.query(Dog).filter(Dog.dog_id == dog_id).first()
            return dog
    

    def update_dog(self, dog_id, chip_id, owner_id, name, birth_date, breed, height, weight, food_per_day, gender, castrated, character, sociable, training, img_url):
        """
        """
        with self.Session() as session:
            dog_to_update = session.query(Dog).filter(Dog.dog_id == dog_id).first()
            dog_to_update.chip_id = chip_id
            dog_to_update.owner_id = owner_id
            dog_to_update.name = name
            dog_to_update.birth_date = birth_date
            dog_to_update.breed = breed
            dog_to_update.height = height
            dog_to_update.weight = weight
            dog_to_update.food_per_day = food_per_day
            dog_to_update.gender = gender
            dog_to_update.castrated = castrated
            dog_to_update.character = character
            dog_to_update.sociable = sociable
            dog_to_update.training = training
            dog_to_update.img_url = img_url
            session.commit()


    def delete_dog(self, dog_id):
        """
        """
        with self.Session() as session:
            dog_to_delete = session.query(Dog).filter(Dog.dog_id == dog_id).first()
            session.delete(dog_to_delete)
            session.commit()


data_manager = SQLiteHandler('pawliday.db')


# create sitter
# data_manager.add_sitter(name="Lina Dahlhaus", email="lina.dahlhaus@icloud.com")

# create owners
# data_manager.add_owner(name="Leo Storm", email="leo.storm@example.com", phone_number="+49 160 55667788")
# data_manager.add_owner(name="Finn Wilder", email="finn.wilder@example.com", phone_number="+49 171 33445566")
# data_manager.add_owner(name="Zara Nightshade", email="zara.nightshade@example.com", phone_number="+49 170 55667788")
# data_manager.add_owner(name="Ivy Blackthorn", email="maya.blackthorn@example.com", phone_number="+49 176 99887766")

# create dogs
# data_manager.add_dog(chip_id=123456789012345, owner_id=1, name="Luna", birth_date="2017-03-15", breed="Mixed breed", height=55, weight=25, food_per_day=500, gender="female", castrated=True, character="sensible", sociable=True, training=True, img_url="https://cdn.pixabay.com/photo/2019/04/05/13/56/shepherd-mongrel-4105106_1280.jpg")
# data_manager.add_dog(chip_id=987654321098765, owner_id=1, name="Max", birth_date="2019-07-22", breed="Golden Retriever", height=60, weight=30, food_per_day=600, gender="male", castrated=False, character="lazy", sociable=True, training=True, img_url="https://cdn.pixabay.com/photo/2020/05/28/17/15/dog-5231903_1280.jpg")
# data_manager.add_dog(chip_id=112233445566778, owner_id=2, name="Bella", birth_date="2020-01-03", breed="Chihuahua", height=25, weight=3, food_per_day=100, gender="female", castrated=False, character="stubborn", sociable=False, training=False, img_url="https://cdn.pixabay.com/photo/2019/01/28/19/18/chihuahua-3961096_1280.jpg")
# data_manager.add_dog(chip_id=223344556677889, owner_id=3, name="Rocky", birth_date="2016-11-09", breed="Border Collie", height=53, weight=20, food_per_day=400, gender="male", castrated=True, character="impulsive", sociable=True, training=True, img_url="https://cdn.pixabay.com/photo/2017/03/29/10/17/border-collie-2184706_1280.jpg")
# data_manager.add_dog(chip_id=556677889900112, owner_id=4, name="Momo", birth_date="2021-10-12", breed="Pomeranian", height=24, weight=3, food_per_day=90, gender="male", castrated=False, character="stubborn", sociable=False, training=True, img_url="https://cdn.pixabay.com/photo/2023/01/19/13/05/pointed-7729054_1280.jpg")
