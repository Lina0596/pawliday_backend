from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Sitter(Base):
    """
    """
    __tablename__ = 'sitters'
    sitter_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)


    def __repr__(self):
        return f'''Sitter(
        sitter_id = {self.sitter_id},
        first_name = {self.first_name},
        last_name = {self.last_name},
        email = {self.email})'''


class Owner(Base):
    """
    """
    __tablename__ = 'owners'
    owner_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    sitter_id = Column(ForeignKey('sitters.sitter_id'), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False, unique=True)


    def __repr__(self):
        return f'''Owner(
        owner_id = {self.owner_id},
        first_name = {self.first_name},
        last_name = {self.last_name},
        email = {self.email},
        phone_number = {self.phone_number})'''


class Dog(Base):
    """
    """
    __tablename__ = 'dogs'
    dog_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    chip_id = Column(Integer, nullable=False, unique=True)
    owner_id = Column(ForeignKey('owners.owner_id'), nullable=False)
    name = Column(String(255), nullable=False)
    birth_date = Column(String(255), nullable=False)
    breed = Column(String(255), nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    food_per_day = Column(Integer, nullable=False)
    gender = Column(String(255), nullable=False)
    castrated = Column(Boolean, nullable=False)
    character = Column(String(255), nullable=False)
    sociable = Column(Boolean, nullable=False)
    training = Column(Boolean, nullable=False)
    img_url = Column(String)


    def __repr__(self):
        return f'''Dog(
        dog_id = {self.dog_id},
        chip_id = {self.chip_id},
        owner_id = {self.owner_id},
        name = {self.name},
        birth_date = {self.birth_date},
        breed = {self.breed},
        height = {self.height},
        weight = {self.weight},
        food_per_day = {self.food_per_day},
        gender = {self.gender},
        castrated = {self.castrated},
        character = {self.character},
        sociable = {self.sociable},
        training = {self.training},
        img_url = {self.img_url})'''


class Trick(Base):
    """
    """
    __tablename__ = 'tricks'
    trick_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    call = Column(String(255), nullable=False)


    def __repr__(self):
        return f'''Trick(
        trick_id = {self.trick_id},
        call = {self.call})'''


class Knowledge(Base):
    """
    """
    __tablename__ = 'knowledges'
    knowledge_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    dog_id = Column(ForeignKey('dogs.dog_id'), nullable=False)
    trick_id = Column(ForeignKey('tricks.trick_id'), nullable=False)
    knowledge = Column(Integer, nullable=False)
    

    def __repr__(self):
        return f'''Knowledge(
        knowledge_id = {self.knowledge_id},
        dog_id = {self.dog_id},
        trick_id = {self.trick_id},
        knowledge = {self.knowledge})'''
    

class Stay(Base):
    """
    """
    __tablename__ = 'stays'
    stay_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    dog_id = Column(ForeignKey('dogs.dog_id'), nullable=False)
    sitter_id = Column(ForeignKey('sitters.sitter_id'), nullable=False)
    checkin = Column(Date, nullable=False)
    checkout = Column(Date, nullable=False)


    def __repr__(self):
        return f'''Stay(
        stay_id = {self.stay_id},
        dog_id = {self.dog_id},
        sitter_id = {self.sitter_id},
        checkin = {self.checkin},
        checkout = {self.checkout})'''
