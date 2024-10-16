from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'fullname')
        read_only_fields = ('is_active', 'is_admin')
