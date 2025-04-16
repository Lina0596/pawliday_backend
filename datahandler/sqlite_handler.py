from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datahandler.abstract_handler import AbstractDataHandler
from datahandler.models import Base, Sitter, Owner, Dog, Stay, Trick, Knowledge
from sqlalchemy.inspection import inspect


def to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


class SQLiteHandler(AbstractDataHandler):
    def __init__(self, db_file_name):
        self.engine = create_engine(f'sqlite:///data/{db_file_name}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)


    def get_all_sitters(self):
        """
        """
        with self.Session() as session:
            sitters_obj = session.query(Sitter).all()
            if not sitters_obj:
                raise LookupError(f"No sitters found.")
            sitters = [to_dict(obj) for obj in sitters_obj]
            return sitters
        

    def add_sitter(self, new_sitter):
        """
        """
        with self.Session() as session:
            new_sitter = Sitter(
                first_name=new_sitter.get('first_name'),
                last_name=new_sitter.get('last_name'),
                email=new_sitter.get('email'),
            )
            session.add(new_sitter)
            session.commit()


    def update_sitter(self, sitter_id, updated_data):
        """
        """
        with self.Session() as session:
            sitter_to_update = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
            if not sitter_to_update:
                raise ValueError(f"No sitter found with id {sitter_id}")
            for key in updated_data:
                setattr(sitter_to_update, key, updated_data.get(key))
            session.commit()


    def get_all_owners(self):
        """
        """
        with self.Session() as session:
            owners_obj = session.query(Owner).all()
            if not owners_obj:
                raise LookupError(f"No owners found.")
            owners = [to_dict(obj) for obj in owners_obj]
            return owners
        
    
    def get_owner(self, owner_id):
        """
        """
        with self.Session() as session:
            owner_obj = session.query(Owner).filter(Owner.owner_id == owner_id).first()
            if not owner_obj:
                raise ValueError(f"No owner found with id {owner_id}")
            owner = to_dict(owner_obj)
            return owner
        
    
    def add_owner(self, new_owner):
        """
        """
        with self.Session() as session:
            new_owner = Owner(
                sitter_id=1,
                first_name=new_owner.get('first_name'),
                last_name=new_owner.get('last_name'),
                email=new_owner.get('email'),
                phone_number=new_owner.get('phone_number')
            )
            session.add(new_owner)
            session.commit()


    def update_owner(self, owner_id, updated_data):
        """
        """
        with self.Session() as session:
            owner_to_update = session.query(Owner).filter(Owner.owner_id == owner_id).first()
            if not owner_to_update:
                raise ValueError(f"No owner found with id {owner_id}")
            for key in updated_data:
                setattr(owner_to_update, key, updated_data.get(key))
            session.commit()


    def delete_owner(self, owner_id):
        """
        """
        with self.Session() as session:
            owner_to_delete = session.query(Owner).filter(Owner.owner_id == owner_id).first()
            if not owner_to_delete:
                raise ValueError(f"No owner found with id {owner_id}")
            dogs_to_delete = session.query(Dog).filter(Dog.owner_id == owner_id).all()
            session.delete(owner_to_delete)
            for dog in dogs_to_delete:
                session.delete(dog)
            session.commit()


    def add_dog(self, owner_id, new_dog):
        """
        """
        with self.Session() as session:
            new_dog = Dog(
                chip_id=new_dog.get('chip_id'),
                owner_id=owner_id,
                name=new_dog.get('name'),
                birth_date=new_dog.get('birth_date'),
                breed=new_dog.get('breed'),
                height=new_dog.get('height'),
                weight=new_dog.get('weight'),
                food_per_day=new_dog.get('food_per_day'),
                gender=new_dog.get('gender'),
                castrated=new_dog.get('castrated'),
                character=new_dog.get('character'),
                sociable=new_dog.get('sociable'),
                training=new_dog.get('training'),
                img_url=new_dog.get('img_url')
            )
            session.add(new_dog)
            session.commit()
    
    
    def get_owner_dogs(self, owner_id):
        """
        """
        with self.Session() as session:
            owner_obj = session.query(Owner).filter(Owner.owner_id == owner_id).first()
            if not owner_obj:
                raise ValueError(f"No owner found with id {owner_id}")
            owner_dogs_obj = session.query(Dog).filter(Dog.owner_id == owner_id).all()
            if not owner_dogs_obj:
                raise LookupError(f"Owner with id {owner_id} has no dogs.")
            owner_dogs = [to_dict(obj) for obj in owner_dogs_obj]
            return owner_dogs
        

    def get_all_dogs(self):
        """
        """
        with self.Session() as session:
            dogs_obj = session.query(Dog).all()
            if not dogs_obj:
                raise LookupError(f"No dogs found.")
            dogs = [to_dict(obj) for obj in dogs_obj]
            return dogs
        

    def get_dog(self, dog_id):
        """
        """
        with self.Session() as session:
            dog_obj = session.query(Dog).filter(Dog.dog_id == dog_id).first()
            if not dog_obj:
                raise ValueError(f"No dog found with id {dog_id}")
            dog = [to_dict(dog_obj)]
            return dog
    

    def update_dog(self, dog_id, updated_data):
        """
        """
        with self.Session() as session:
            dog_to_update = session.query(Dog).filter(Dog.dog_id == dog_id).first()
            if not dog_to_update:
                raise ValueError(f"No dog found with id {dog_id}")
            for key in updated_data:
                setattr(dog_to_update, key, updated_data.get(key))
            session.commit()


    def delete_dog(self, dog_id):
        """
        """
        with self.Session() as session:
            dog_to_delete = session.query(Dog).filter(Dog.dog_id == dog_id).first()
            if not dog_to_delete:
                raise ValueError(f"No dog found with id {dog_id}")
            session.delete(dog_to_delete)
            session.commit()


# create database
# data_manager = SQLiteHandler('pawliday.db')

# create sitters
# data_manager.add_sitter({"first_name": "Lina", "last_name": "Dahlhaus", "email": "lina.dahlhaus@icloud.com"})

# create owners
# data_manager.add_owner({"first_name": "Leo", "last_name": "Storm", "email": "leo.storm@example.com", "phone_number": "004916055667788"})
# data_manager.add_owner({"first_name": "Finn", "last_name": "Wilder", "email": "finn.wilder@example.com", "phone_number": "004917133445566"})
# data_manager.add_owner({"first_name": "Zara", "last_name": "Nightshade", "email": "zara.nightshade@example.com", "phone_number": "004917055667788"})
# data_manager.add_owner({"first_name": "Ivy", "last_name": "Blackthorn", "email": "maya.blackthorn@example.com", "phone_number": "004917699887766"})
# data_manager.add_owner({"first_name": "Kai", "last_name": "Ironhart", "email": "kai.ironhart@example.com", "phone_number": "004915744556677"})
# data_manager.add_owner({"first_name": "Nova", "last_name": "Winters", "email": "nova.winters@example.com", "phone_number": "004915277889911"})
# data_manager.add_owner({"first_name": "Selene", "last_name": "Shadowbrook", "email": "selene.shadowbrook@example.com", "phone_number": "004917033442211"})

# create dogs
# data_manager.add_dog(owner_id=1, new_dog={"chip_id": 123456789012345, "name": "Luna", "birth_date": "2017-03-15", "breed": "Mixed breed", "height": 55, "weight": 25, "food_per_day": 500, "gender": "female", "castrated": True, "character": "sensible", "sociable": True, "training": True, "img_url": "https://cdn.pixabay.com/photo/2019/04/05/13/56/shepherd-mongrel-4105106_1280.jpg"})
# data_manager.add_dog(owner_id=1, new_dog={"chip_id": 987654321098765, "name": "Max", "birth_date": "2019-07-22", "breed": "Golden Retriever", "height": 60, "weight": 30, "food_per_day": 600, "gender": "male", "castrated": False, "character": "lazy", "sociable": True, "training": True, "img_url": "https://cdn.pixabay.com/photo/2020/05/28/17/15/dog-5231903_1280.jpg"})
# data_manager.add_dog(owner_id=2, new_dog={"chip_id": 112233445566778, "name": "Bella", "birth_date": "2020-01-03", "breed": "Chihuahua", "height": 25, "weight": 3, "food_per_day": 100, "gender": "female", "castrated": False, "character": "stubborn", "sociable": False, "training": False, "img_url": "https://cdn.pixabay.com/photo/2019/01/28/19/18/chihuahua-3961096_1280.jpg"})
# data_manager.add_dog(owner_id=3, new_dog={"chip_id": 223344556677889, "name": "Rocky", "birth_date": "2016-11-09", "breed": "Border Collie", "height": 53, "weight": 20, "food_per_day": 400, "gender": "male", "castrated": True, "character": "impulsive", "sociable": True, "training": True, "img_url": "https://cdn.pixabay.com/photo/2017/03/29/10/17/border-collie-2184706_1280.jpg"})
# data_manager.add_dog(owner_id=4, new_dog={"chip_id": 556677889900112, "name": "Momo", "birth_date": "2021-10-12", "breed": "Pomeranian", "height": 24, "weight": 3, "food_per_day": 90, "gender": "male", "castrated": False, "character": "stubborn", "sociable": False, "training": True, "img_url": "https://cdn.pixabay.com/photo/2023/01/19/13/05/pointed-7729054_1280.jpg"})
# data_manager.add_dog(owner_id=5, new_dog={"chip_id": 445566778899001, "name": "Bruno", "birth_date": "2018-02-17", "breed": "Bernese Mountain Dog", "height": 65, "weight": 38, "food_per_day": 750, "gender": "male", "castrated": False, "character": "lazy", "sociable": True, "training": False, "img_url": "https://cdn.pixabay.com/photo/2020/11/21/08/34/bernese-mountain-dog-5763415_1280.jpg"})
# data_manager.add_dog(owner_id=5, new_dog={"chip_id": 667788990011223, "name": "Heidi", "birth_date": "2019-04-04", "breed": "Bernese Mountain Dog", "height": 63, "weight": 36, "food_per_day": 700, "gender": "female", "castrated": True, "character": "sensible", "sociable": True, "training": False, "img_url": "https://cdn.pixabay.com/photo/2016/02/01/12/25/dog-1173509_1280.jpg"})
# data_manager.add_dog(owner_id=6, new_dog={"chip_id": 778899001122334, "name": "Koda", "birth_date": "2020-12-08", "breed": "Siberian Husky", "height": 59, "weight": 23, "food_per_day": 600, "gender": "male", "castrated": True, "character": "impulsive", "sociable": False, "training": True, "img_url": "https://cdn.pixabay.com/photo/2020/03/11/13/45/snow-4922199_1280.jpg"})
# data_manager.add_dog(owner_id=7, new_dog={"chip_id": 889900112233445, "name": "Coco", "birth_date": "2021-06-21", "breed": "Royal Poodle", "height": 45, "weight": 18, "food_per_day": 350, "gender": "female", "castrated": False, "character": "sensible", "sociable": True, "training": False, "img_url": "https://cdn.pixabay.com/photo/2016/08/01/15/58/poodle-1561405_1280.jpg"})
