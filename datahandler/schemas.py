from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional
import phonenumbers
from exceptions import InvalidInputError
from typing import Any


class SitterSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UpdateSitterSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True


class OwnerSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str


    @field_validator("phone_number", mode="before")
    def validate_and_format_phone_number(cls, value: str) -> str:
        try:
            number = phonenumbers.parse(value, "DE")
            if not phonenumbers.is_valid_number(number):
                raise InvalidInputError("Invalid phone number for Germany")
            return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise InvalidInputError("Phone number could not be validated")

    class Config:
        from_attribute = True


class UpdateOwnerSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    @field_validator("phone_number")
    def validate_and_format_phone_number(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        try:
            number = phonenumbers.parse(value, "DE")
            if not phonenumbers.is_valid_number(number):
                raise InvalidInputError("Invalid phone number for Germany")
            return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise InvalidInputError("Phone number could not be validated")

    class Config:
        from_attribute = True


class DogSchema(BaseModel):
    chip_id: int
    name: str
    birth_date: date
    breed: str
    height: int
    weight: int
    food_per_day: int
    gender: str
    castrated: bool
    character: str
    sociable: bool
    training: bool
    img_url: str

    class Config:
        from_attribute = True


class UpdateDogSchema(BaseModel):
    chip_id: Optional[int]
    name: Optional[str]
    birth_date: Optional[date]
    breed: Optional[str]
    height: Optional[int]
    weight: Optional[int]
    food_per_day: Optional[int]
    gender: Optional[str]
    castrated: Optional[bool]
    character: Optional[str]
    sociable: Optional[bool]
    training: Optional[bool]
    img_url: Optional[str]

    class Config:
        from_attribute = True
