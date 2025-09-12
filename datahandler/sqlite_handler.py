import sys
import os


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datahandler.abstract_handler import AbstractDataHandler
from datahandler.models import Base, Sitter, Owner, Dog, Stay, Skill, Knowledge
from sqlalchemy.inspection import inspect
from datahandler.schemas import SitterSchema, UpdateSitterSchema, LoginSchema, OwnerSchema, UpdateOwnerSchema, DogSchema, UpdateDogSchema
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import ValidationError
from exceptions import NotFoundError, InvalidInputError, DatabaseError
from bcrypt import hashpw, gensalt, checkpw


def to_dict(obj):
    dict_obj = {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
    dict_obj.pop('password', None)
    return dict_obj


class SQLiteHandler(AbstractDataHandler):
    def __init__(self, db_file_name):
        self.engine = create_engine(f'sqlite:///data/{db_file_name}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)


    def authenticate_sitter(self, login_data):
        try:
            with self.Session.begin() as session:
                valid_data = LoginSchema(**login_data)
                sitter_obj = session.query(Sitter).filter(Sitter.email == valid_data.email).first()
                if not sitter_obj:
                    raise InvalidInputError("Email or password is wrong")
                if checkpw(valid_data.password.encode('utf-8'), sitter_obj.password.encode('utf-8')):
                    sitter = to_dict(sitter_obj)
                    return sitter
                else:
                    raise InvalidInputError("Email or password is wrong")
        except ValidationError:
            raise InvalidInputError("Invalid input")
        except OperationalError:
            raise DatabaseError("Database unavailable")        
        
        
    def get_sitter(self, sitter_id):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                sitter = to_dict(sitter_obj)
                return sitter
        except OperationalError:
            raise DatabaseError("Database unavailable")
        

    def add_sitter(self, new_sitter_data):
        try:
            with self.Session.begin() as session:
                valid_data = SitterSchema(**new_sitter_data)
                hashed_password = hashpw(valid_data.password.encode('utf-8'), gensalt())
                new_sitter = Sitter(
                    first_name=valid_data.first_name,
                    last_name=valid_data.last_name,
                    email=valid_data.email,
                    password=hashed_password.decode('utf-8')
                )
                session.add(new_sitter)
                session.flush()
                created_sitter = to_dict(new_sitter)
                return created_sitter
        except IntegrityError:
            raise InvalidInputError("Email already exists")
        except ValidationError:
            raise InvalidInputError("Invalid input")
        except OperationalError:
            raise DatabaseError("Database unavailable")
        

    def update_sitter(self, sitter_id, updated_data):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_to_update = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_to_update:
                    raise NotFoundError("No sitter found")
                valid_updated_data = UpdateSitterSchema(**updated_data).model_dump(exclude_unset=True)
                if 'password' in valid_updated_data:
                    hashed_password = hashpw(valid_updated_data['password'].encode('utf-8'), gensalt())
                    valid_updated_data['password'] = hashed_password.decode('utf-8')
                for key, value in valid_updated_data.items():
                    setattr(sitter_to_update, key, value)
                updated_sitter = to_dict(sitter_to_update)
            return updated_sitter
        except IntegrityError:
            raise InvalidInputError("Email already exists")
        except ValidationError:
            raise InvalidInputError("Invalid input")
        except OperationalError:
            raise DatabaseError("Database unavailable")


    def delete_sitter(self, sitter_id):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_to_delete = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_to_delete:
                    raise NotFoundError("No sitter found")
                dogs_to_delete = session.query(Dog).join(Owner).filter(Owner.sitter_id == sitter_id).all()
                for dog in dogs_to_delete:
                    session.delete(dog)
                owners_to_delete = session.query(Owner).filter(Owner.sitter_id == sitter_id).all()
                for owner in owners_to_delete:
                    session.delete(owner)
                session.delete(sitter_to_delete)
                session.commit()
        except OperationalError:
            raise DatabaseError("Database unavailable")


    def get_all_owners(self, sitter_id):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                owners_obj = session.query(Owner).filter(Owner.sitter_id == sitter_id).all()
                if not owners_obj:
                    raise NotFoundError("No owners found")
                owners = [to_dict(obj) for obj in owners_obj]
                return owners
        except OperationalError:
            raise DatabaseError("Database unavailable")
        
    
    def get_owner(self, sitter_id, owner_id):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                if not owner_id.isdigit():
                    raise InvalidInputError("owner_id must be a number")
                owner_obj = session.query(Owner).filter(Owner.owner_id == owner_id, Owner.sitter_id == sitter_id).first()
                if not owner_obj:
                    raise NotFoundError("No owner found")
                owner = to_dict(owner_obj)
                return owner
        except OperationalError:
            raise DatabaseError("Database unavailable")
        
    
    def add_owner(self, sitter_id, new_owner_data):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                valid_data = OwnerSchema(**new_owner_data)
                new_owner = Owner(
                    sitter_id=sitter_id,
                    first_name=valid_data.first_name,
                    last_name=valid_data.last_name,
                    email=valid_data.email,
                    phone_number=valid_data.phone_number
                )
                session.add(new_owner)
                session.flush()
                created_owner = to_dict(new_owner)
                return created_owner
        except IntegrityError:
            raise InvalidInputError("Email or phone number already exists")
        except ValidationError:
            raise InvalidInputError("Invalid input")
        except OperationalError:
            raise DatabaseError("Database unavailable")


    def update_owner(self, sitter_id, owner_id, updated_data):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                if not owner_id.isdigit():
                    raise InvalidInputError("owner_id must be a number")
                owner_to_update = session.query(Owner).filter(Owner.owner_id == owner_id, Owner.sitter_id == sitter_id).first()
                if not owner_to_update:
                    raise NotFoundError("No owner found")
                valid_updated_data = UpdateOwnerSchema(**updated_data).model_dump(exclude_unset=True)
                for key, value in valid_updated_data.items():
                    setattr(owner_to_update, key, value)
                session.commit()
        except IntegrityError:
            raise InvalidInputError("Email or phone number already exists")
        except ValidationError:
            raise InvalidInputError("Invalid input")
        except OperationalError:
            raise DatabaseError("Database unavailable")


    def delete_owner(self, sitter_id, owner_id):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                if not owner_id.isdigit():
                    raise InvalidInputError("owner_id must be a number")
                owner_to_delete = session.query(Owner).filter(Owner.owner_id == owner_id, Owner.sitter_id == sitter_id).first()
                if not owner_to_delete:
                    raise NotFoundError("No owner found")
                dogs_to_delete = session.query(Dog).filter(Dog.owner_id == owner_id).all()
                for dog in dogs_to_delete:
                    session.delete(dog)
                session.delete(owner_to_delete)
                session.commit()
        except OperationalError:
            raise DatabaseError("Database unavailable")
        

    def get_all_dogs(self, sitter_id):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                dogs_obj = session.query(Dog).join(Owner).filter(Owner.sitter_id == sitter_id).all()
                if not dogs_obj:
                    raise NotFoundError("No dogs found")
                dogs = [to_dict(obj) for obj in dogs_obj]
                return dogs
        except OperationalError:
            raise DatabaseError("Database unavailable")
        

    def get_dog(self, sitter_id, dog_id):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                if not dog_id.isdigit():
                    raise InvalidInputError("dog_id must be a number")
                dog_obj = session.query(Dog).join(Owner).filter(Dog.dog_id == dog_id, Owner.sitter_id == sitter_id).first()
                if not dog_obj:
                    raise NotFoundError("No dog found")
                dog = to_dict(dog_obj)
                return dog
        except OperationalError:
            raise DatabaseError("Database unavailable")

    
    def add_dog(self, sitter_id, owner_id, new_dog_data):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                if not owner_id.isdigit():
                    raise InvalidInputError("owner_id must be a number")
                owner_obj = session.query(Owner).filter(Owner.owner_id == owner_id, Owner.sitter_id == sitter_id).first()
                if not owner_obj:
                    raise NotFoundError("No owner found")
                valid_data = DogSchema(**new_dog_data)
                new_dog = Dog(
                    chip_id=valid_data.chip_id,
                    owner_id=owner_id,
                    name=valid_data.name,
                    birth_date=valid_data.birth_date,
                    breed=valid_data.breed,
                    height=valid_data.height,
                    weight=valid_data.weight,
                    food_per_day=valid_data.food_per_day,
                    gender=valid_data.gender,
                    castrated=valid_data.castrated,
                    character=valid_data.character,
                    sociable=valid_data.sociable,
                    training=valid_data.training,
                    img_url=valid_data.img_url
                )
                session.add(new_dog)
                session.flush()
                created_dog = to_dict(new_dog)
                return created_dog
        except IntegrityError:
            raise InvalidInputError("chip id already exists")
        except ValidationError:
            raise InvalidInputError("Invalid input")
        except OperationalError:
            raise DatabaseError("Database unavailable")
    

    def update_dog(self, sitter_id, dog_id, updated_data):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                if not dog_id.isdigit():
                    raise InvalidInputError("dog_id must be a number")
                dog_to_update = session.query(Dog).join(Owner).filter(Dog.dog_id == dog_id, Owner.sitter_id == sitter_id).first()
                if not dog_to_update:
                    raise NotFoundError("No dog found")
                valid_updated_data = UpdateDogSchema(**updated_data).model_dump(exclude_unset=True)
                for key, value in valid_updated_data.items():
                    setattr(dog_to_update, key, value)
                session.commit()
        except IntegrityError:
            raise InvalidInputError("chip id already exists")
        except ValidationError:
            raise InvalidInputError("Invalid input")
        except OperationalError:
            raise DatabaseError("Database unavailable")


    def delete_dog(self, sitter_id, dog_id):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                if not dog_id.isdigit():
                    raise InvalidInputError("dog_id must be a number")
                dog_to_delete = session.query(Dog).join(Owner).filter(Dog.dog_id == dog_id, Owner.sitter_id == sitter_id).first()
                if not dog_to_delete:
                    raise NotFoundError("No dog found")
                session.delete(dog_to_delete)
                session.commit()
        except OperationalError:
            raise DatabaseError("Database unavailable")
        

    def get_owner_dogs(self, sitter_id, owner_id,):
        try:
            with self.Session.begin() as session:
                if not sitter_id.isdigit():
                    raise InvalidInputError("sitter_id must be a number")
                sitter_obj = session.query(Sitter).filter(Sitter.sitter_id == sitter_id).first()
                if not sitter_obj:
                    raise NotFoundError("No sitter found")
                if not owner_id.isdigit():
                    raise InvalidInputError("owner_id must be a number")
                owner_obj = session.query(Owner).filter(Owner.owner_id == owner_id).first()
                if not owner_obj:
                    raise NotFoundError("No owner found")
                owner_dogs_obj = session.query(Dog).join(Owner).filter(Owner.owner_id == owner_id, Owner.sitter_id == sitter_id).all()
                if not owner_dogs_obj:
                    raise NotFoundError("No dogs found")
                owner_dogs = [to_dict(obj) for obj in owner_dogs_obj]
                return owner_dogs
        except OperationalError:
            raise DatabaseError("Database unavailable")


# create database
# data_manager = SQLiteHandler('pawliday.db')

# create sitters
# data_manager.add_sitter(new_sitter_data={"first_name": "Emily", "last_name": "Johnson", "email": "emily.johnson@example.com", "password": "sitter1"})
# data_manager.add_sitter(new_sitter_data={"first_name": "David", "last_name": "Wilson", "email": "david.wilson@example.com", "password": "sitter2"})
# data_manager.add_sitter(new_sitter_data={"first_name": "Sarah", "last_name": "Davis", "email": "sarah.davis@example.com", "password": "sitter3"})

# create owners
# data_manager.add_owner(sitter_id="1", new_owner_data={"first_name": "Leo", "last_name": "Storm", "email": "leo.storm@example.com", "phone_number": "+49 163 2438301"})
# data_manager.add_owner(sitter_id="1", new_owner_data={"first_name": "Finn", "last_name": "Wilder", "email": "finn.wilder@example.com", "phone_number": "+49 177 8297922"})
# data_manager.add_owner(sitter_id="1", new_owner_data={"first_name": "Zara", "last_name": "Nightshade", "email": "zara.nightshade@example.com", "phone_number": "+49 178 7069665"})
# data_manager.add_owner(sitter_id="1", new_owner_data={"first_name": "Ivy", "last_name": "Blackthorn", "email": "maya.blackthorn@example.com", "phone_number": "+49 175 6341714"})
# data_manager.add_owner(sitter_id="2", new_owner_data={"first_name": "Kai", "last_name": "Ironhart", "email": "kai.ironhart@example.com", "phone_number": "+49 171 0006303"})
# data_manager.add_owner(sitter_id="2", new_owner_data={"first_name": "Nova", "last_name": "Winters", "email": "nova.winters@example.com", "phone_number": "+49 171 3903711"})
# data_manager.add_owner(sitter_id="2", new_owner_data={"first_name": "Selene", "last_name": "Shadowbrook", "email": "selene.shadowbrook@example.com", "phone_number": "+49 170 1373380"})

# create dogs
# data_manager.add_dog(sitter_id="1", owner_id="1", new_dog_data={"chip_id": 123456789012345, "name": "Luna", "birth_date": "2017-03-15", "breed": "Mixed breed", "height": 55, "weight": 25, "food_per_day": 500, "gender": "female", "castrated": True, "character": "sensible", "sociable": True, "training": True, "img_url": "https://cdn.pixabay.com/photo/2019/04/05/13/56/shepherd-mongrel-4105106_1280.jpg"})
# data_manager.add_dog(sitter_id="1", owner_id="1", new_dog_data={"chip_id": 987654321098765, "name": "Max", "birth_date": "2019-07-22", "breed": "Golden Retriever", "height": 60, "weight": 30, "food_per_day": 600, "gender": "male", "castrated": False, "character": "lazy", "sociable": True, "training": True, "img_url": "https://cdn.pixabay.com/photo/2020/05/28/17/15/dog-5231903_1280.jpg"})
# data_manager.add_dog(sitter_id="1", owner_id="2", new_dog_data={"chip_id": 112233445566778, "name": "Bella", "birth_date": "2020-01-03", "breed": "Chihuahua", "height": 25, "weight": 3, "food_per_day": 100, "gender": "female", "castrated": False, "character": "stubborn", "sociable": False, "training": False, "img_url": "https://cdn.pixabay.com/photo/2019/01/28/19/18/chihuahua-3961096_1280.jpg"})
# data_manager.add_dog(sitter_id="1", owner_id="3", new_dog_data={"chip_id": 223344556677889, "name": "Rocky", "birth_date": "2016-11-09", "breed": "Border Collie", "height": 53, "weight": 20, "food_per_day": 400, "gender": "male", "castrated": True, "character": "impulsive", "sociable": True, "training": True, "img_url": "https://cdn.pixabay.com/photo/2017/03/29/10/17/border-collie-2184706_1280.jpg"})
# data_manager.add_dog(sitter_id="1", owner_id="4", new_dog_data={"chip_id": 556677889900112, "name": "Momo", "birth_date": "2021-10-12", "breed": "Pomeranian", "height": 24, "weight": 3, "food_per_day": 90, "gender": "male", "castrated": False, "character": "stubborn", "sociable": False, "training": True, "img_url": "https://cdn.pixabay.com/photo/2023/01/19/13/05/pointed-7729054_1280.jpg"})
# data_manager.add_dog(sitter_id="2", owner_id="5", new_dog_data={"chip_id": 445566778899001, "name": "Bruno", "birth_date": "2018-02-17", "breed": "Bernese Mountain Dog", "height": 65, "weight": 38, "food_per_day": 750, "gender": "male", "castrated": False, "character": "lazy", "sociable": True, "training": False, "img_url": "https://cdn.pixabay.com/photo/2020/11/21/08/34/bernese-mountain-dog-5763415_1280.jpg"})
# data_manager.add_dog(sitter_id="2", owner_id="5", new_dog_data={"chip_id": 667788990011223, "name": "Heidi", "birth_date": "2019-04-04", "breed": "Bernese Mountain Dog", "height": 63, "weight": 36, "food_per_day": 700, "gender": "female", "castrated": True, "character": "sensible", "sociable": True, "training": False, "img_url": "https://cdn.pixabay.com/photo/2016/02/01/12/25/dog-1173509_1280.jpg"})
# data_manager.add_dog(sitter_id="2", owner_id="6", new_dog_data={"chip_id": 778899001122334, "name": "Koda", "birth_date": "2020-12-08", "breed": "Siberian Husky", "height": 59, "weight": 23, "food_per_day": 600, "gender": "male", "castrated": True, "character": "impulsive", "sociable": False, "training": True, "img_url": "https://cdn.pixabay.com/photo/2020/03/11/13/45/snow-4922199_1280.jpg"})
# data_manager.add_dog(sitter_id="2", owner_id="7", new_dog_data={"chip_id": 889900112233445, "name": "Coco", "birth_date": "2021-06-21", "breed": "Royal Poodle", "height": 45, "weight": 18, "food_per_day": 350, "gender": "female", "castrated": False, "character": "sensible", "sociable": True, "training": False, "img_url": "https://cdn.pixabay.com/photo/2016/08/01/15/58/poodle-1561405_1280.jpg"})
