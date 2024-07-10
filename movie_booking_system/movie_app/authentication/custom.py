import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from .blacklist import BlacklistedToken

logger = logging.getLogger(__name__)

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        logger.info(f"Headers received: {request.headers}")
        
        header = self.get_header(request)
        if header is None:
            logger.warning("Authorization header not found")
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            logger.warning("Raw token not found in header")
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except InvalidToken as e:
            logger.error(f"Token validation failed: {str(e)}")
            raise

        if BlacklistedToken.is_blacklisted(str(validated_token)):
            logger.warning("Token is blacklisted")
            raise AuthenticationFailed('Token is blacklisted', code='token_blacklisted')

        user = self.get_user(validated_token)
        logger.info(f"Authentication successful for user: {user}")
        return user, validated_token