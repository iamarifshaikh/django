from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class BlacklistedToken(Document):
    token = StringField(required=True, unique=True)
    blacklisted_at = DateTimeField(default=datetime.utcnow)

    @classmethod
    def is_blacklisted(cls, token):
        return cls.objects(token=token).first() is not None

    @classmethod
    def blacklist(cls, token):
        if not cls.is_blacklisted(token):
            cls(token=token).save()