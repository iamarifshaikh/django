from mongoengine import Document, StringField, EmailField, DateTimeField
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

# Create your models here.
class User(Document):
    name = StringField(required=True, max_length=150, unique=True)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    dateOfRegisteration = DateTimeField(default=timezone.now)
    
    def set_password(self,raw_password):
        logger.info(f"Setting password for user {self.name}")
        self.password = make_password(raw_password)
        logger.info(f"Password hash: {self.password[:10]}...")  
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        logger.info(f"Saving user {self.name}")
        logger.info(f"User fields: name={self.name}, email={self.email}, password_set={'Yes' if self.password else 'No'}")
        super(User, self).save(*args, **kwargs)
        logger.info(f"User {self.name} saved successfully")