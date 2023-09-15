import re
from pydantic import BaseModel, Field, validator
from typing import List


class Name(BaseModel):
    firstName: str = Field(
        description="Ensure that this first name is valid by checking for only letters, spaces, hyphens, and apostrophes."
    )
    lastName: str = Field(
        description="Ensure that this last name is valid by checking for only letters, spaces, hyphens, and apostrophes."
    )

    @validator("firstName")
    def is_valid_name(name):
        # Regular expression pattern to match valid names
        pattern = r"^[A-Za-z]+(?:[\s-][A-Za-z]+)*$"
        is_valid = bool(re.match(pattern, name))
        if is_valid == False:
            raise ValueError("This is not a correct answer")
        return name

    @validator("lastName")
    def is_valid_lastname(name):
        # Regular expression pattern to match valid names
        pattern = r"^[A-Za-z]+(?:[\s-][A-Za-z]+)*$"
        is_valid = bool(re.match(pattern, name))
        if is_valid == False:
            raise ValueError("This is not a correct answer")
        return name


class BookingNumber(BaseModel):
    bookingNumber: str = Field(
        description="6-digit flight code that is a mix of numbers that identifies their booking."
    )

    @validator("bookingNumber")
    def is_valid_bookingNumber(bookingNumber):
        pattern = r"^[A-Za-z0-9]{6}$"
        is_valid = bool(re.match(pattern, bookingNumber))
        if is_valid == False:
            raise ValueError("This is not a correct answer")
        return bookingNumber
