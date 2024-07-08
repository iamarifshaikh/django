import re
from mongoengine import Document,StringField,EmailField, errors, IntField

def validate_password(password):
    # At least one uppercase letter
    if not re.search(r'[A-Z]', password):
        raise errors.ValidationError("Password must contain at least one uppercase letter.")
    # At least one symbol
    if not re.search(r'[\W_]', password):
        raise errors.ValidationError("Password must contain at least one symbol.")
    # At least one number
    if not re.search(r'\d', password):
        raise errors.ValidationError("Password must contain at least one number.")
    # Minimum length of 8 characters
    if len(password) < 8:
        raise errors.ValidationError("Password must be at least 8 characters long.")

# Create your models here.
class User(Document):
    name = StringField(required = True,max_length=50)
    email = EmailField(required = True, unique = True)
    number = StringField(required=False)
    password = StringField(required = True,validation=validate_password)