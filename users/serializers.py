from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "name",
            "email",
            "is_active",
            "is_staff",
        )
