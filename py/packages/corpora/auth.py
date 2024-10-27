from ninja.security import HttpBearer
from oauth2_provider.models import AccessToken
from django.utils import timezone


class BearerAuth(HttpBearer):
    async def authenticate(self, request, token):
        try:
            access_token = await AccessToken.objects.select_related("user").aget(
                token=token, expires__gt=timezone.now()
            )
            request.user = access_token.user
            return access_token.user
        except AccessToken.DoesNotExist:
            return None
