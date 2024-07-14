from mongoengine import Document, StringField, DateTimeField, ImageField, DateField, EnumField
from enum import Enum

class LanguageEnum(Enum):
    ENGLISH = "English"
    HINDI = "Hindi"
    SPANISH = "Spanish"
    FRENCH = "French"
    GERMAN = "German"
    CHINESE = "Chinese"
    TELUGU = "Telugu"
    TAMIL = "Tamil"
    BENGALI = "Bengali"
    ITALIAN = "Italian"
    DUTCH = "Dutch"
    MARATHI = "Marathi"

class GenreEnum(Enum):
    ACTION = "Action"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    HORROR = "Horror"
    ROMANCE = "Romance"
    THRILLER = "Thriller"
    SCIFI = "Sci-Fi"
    FANTASY = "Fantasy"
    ANIMATION = "Animation"
    DOCUMENTARY = "Documentary"
    MYSTERY = "Mystery"
    BIOGRAPHY = "Biography"
    MUSICAL = "Musical"
    ADVENTURE = "Adventure"


# Create your models here
class Movies(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    language = EnumField(LanguageEnum,required=True)
    genre = EnumField(GenreEnum,required=True)
    poster = ImageField(required=True)
    release_date = DateField(required=True)