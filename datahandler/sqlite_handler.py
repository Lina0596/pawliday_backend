from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datahandler.abstract_handler import AbstractDataHandler
from datahandler.models import Base, Sitter, Owner, Dog, Stay, Trick, Knowledge
from sqlalchemy.inspection import inspect
import json


def to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


class SQLiteHandler(AbstractDataHandler):
    def __init__(self, db_file_name):
        self.engine = create_engine(f'sqlite:///data/{db_file_name}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)


    def get_all_owners(self):
        """
        """
        with self.Session() as session:
            owners_obj = session.query(Owner).all()
            owners = [to_dict(obj) for obj in owners_obj]
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
            dogs_to_delete = session.query(Dog).filter(Dog.owner_id == owner_id).all()
            session.delete(owner_to_delete)
            for dog in dogs_to_delete:
                session.delete(dog)
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
            owner_dogs_obj = session.query(Dog).filter(Dog.owner_id == owner_id).all()
            owner_dogs = [to_dict(obj) for obj in owner_dogs_obj]
            return owner_dogs
        

    def get_dog(self, dog_id):
        """
        """
        with self.Session() as session:
            dog_obj = session.query(Dog).filter(Dog.dog_id == dog_id).first()
            dog = to_dict(dog_obj)
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


# data_manager = SQLiteHandler('pawliday.db')

# create sitter
# data_manager.add_sitter(name="Lina Dahlhaus", email="lina.dahlhaus@icloud.com")

# create owners
# data_manager.add_owner(name="Leo Storm", email="leo.storm@example.com", phone_number="+49 160 55667788")
# data_manager.add_owner(name="Finn Wilder", email="finn.wilder@example.com", phone_number="+49 171 33445566")
# data_manager.add_owner(name="Zara Nightshade", email="zara.nightshade@example.com", phone_number="+49 170 55667788")
# data_manager.add_owner(name="Ivy Blackthorn", email="maya.blackthorn@example.com", phone_number="+49 176 99887766")
# data_manager.add_owner(name="Kai Ironhart", email="kai.ironhart@example.com", phone_number="+49 157 44556677")
# data_manager.add_owner(name="Nova Winters", email="nova.winters@example.com", phone_number="+49 152 77889911")
# data_manager.add_owner(name="Selene Shadowbrook", email="selene.shadowbrook@example.com", phone_number="+49 170 33442211")

# create dogs
# data_manager.add_dog(chip_id=123456789012345, owner_id=1, name="Luna", birth_date="2017-03-15", breed="Mixed breed", height=55, weight=25, food_per_day=500, gender="female", castrated=True, character="sensible", sociable=True, training=True, img_url="https://cdn.pixabay.com/photo/2019/04/05/13/56/shepherd-mongrel-4105106_1280.jpg")
# data_manager.add_dog(chip_id=987654321098765, owner_id=1, name="Max", birth_date="2019-07-22", breed="Golden Retriever", height=60, weight=30, food_per_day=600, gender="male", castrated=False, character="lazy", sociable=True, training=True, img_url="https://cdn.pixabay.com/photo/2020/05/28/17/15/dog-5231903_1280.jpg")
# data_manager.add_dog(chip_id=112233445566778, owner_id=2, name="Bella", birth_date="2020-01-03", breed="Chihuahua", height=25, weight=3, food_per_day=100, gender="female", castrated=False, character="stubborn", sociable=False, training=False, img_url="https://cdn.pixabay.com/photo/2019/01/28/19/18/chihuahua-3961096_1280.jpg")
# data_manager.add_dog(chip_id=223344556677889, owner_id=3, name="Rocky", birth_date="2016-11-09", breed="Border Collie", height=53, weight=20, food_per_day=400, gender="male", castrated=True, character="impulsive", sociable=True, training=True, img_url="https://cdn.pixabay.com/photo/2017/03/29/10/17/border-collie-2184706_1280.jpg")
# data_manager.add_dog(chip_id=556677889900112, owner_id=4, name="Momo", birth_date="2021-10-12", breed="Pomeranian", height=24, weight=3, food_per_day=90, gender="male", castrated=False, character="stubborn", sociable=False, training=True, img_url="https://cdn.pixabay.com/photo/2023/01/19/13/05/pointed-7729054_1280.jpg")
# data_manager.add_dog(chip_id=445566778899001, owner_id=5, name="Bruno", birth_date="2018-02-17", breed="Bernese Mountain Dog", height=65, weight=38, food_per_day=750, gender="male", castrated=False, character="lazy", sociable=True, training=False, img_url="https://cdn.pixabay.com/photo/2020/11/21/08/34/bernese-mountain-dog-5763415_1280.jpg")
# data_manager.add_dog(chip_id=667788990011223, owner_id=5, name="Heidi", birth_date="2019-04-04", breed="Bernese Mountain Dog", height=63, weight=36, food_per_day=700, gender="female", castrated=True, character="sensible", sociable=True, training=False, img_url="https://cdn.pixabay.com/photo/2016/02/01/12/25/dog-1173509_1280.jpg")
# data_manager.add_dog(chip_id=778899001122334, owner_id=6, name="Koda", birth_date="2020-12-08", breed="Siberian Husky", height=59, weight=23, food_per_day=600, gender="male", castrated=True, character="impulsive", sociable=False, training=True, img_url="https://cdn.pixabay.com/photo/2020/03/11/13/45/snow-4922199_1280.jpg")
# data_manager.add_dog(chip_id=889900112233445, owner_id=7, name="Coco", birth_date="2021-06-21", breed="Royal Poodle", height=45, weight=18, food_per_day=350, gender="female", castrated=False, character="sensible", sociable=True, training=False, img_url="https://cdn.pixabay.com/photo/2016/08/01/15/58/poodle-1561405_1280.jpg")
