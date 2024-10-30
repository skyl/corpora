from asgiref.sync import sync_to_async
from ninja.security import HttpBearer
from oauth2_provider.models import AccessToken
from django.utils import timezone


class BearerAuth(HttpBearer):
    async def authenticate(self, request, token):
        # print("TOKEN", token)
        try:
            access_token = await AccessToken.objects.select_related(
                "user",
                "application",
            ).aget(token=token, expires__gt=timezone.now())
            # HRM: client credential bearer is the owner of the application
            # in 3LO, the user is the owner of the token
            if (
                access_token.application.authorization_grant_type
                == "client-credentials"
            ):
                user = await sync_to_async(lambda: access_token.application.user)()
                request.user = user
                return user

            return access_token.user
        except AccessToken.DoesNotExist:
            # print("NO AUTH")
            return None
