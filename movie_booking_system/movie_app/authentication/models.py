# models.py
from mongoengine import Document, StringField, EmailField, DateTimeField
import bcrypt
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

# Create your models here.
class User(Document):
    name = StringField(required=True, max_length=150, unique=True)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    date_of_registration = DateTimeField(default=timezone.now)
    
    def set_password(self, raw_password):
        logger.info(f"Setting password for user {self.name}")
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), salt).decode('utf-8')
        logger.info(f"Password hash: {self.password[:10]}...")
        
    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
    
    def save(self, *args, **kwargs):
        logger.info(f"Saving user {self.name}")
        logger.info(f"User fields: name={self.name}, email={self.email}, password_set={'Yes' if self.password else 'No'}")
        super(User, self).save(*args, **kwargs)
        logger.info(f"User {self.name} saved successfully")