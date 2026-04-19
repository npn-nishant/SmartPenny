from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(default='parent')

    class Meta:
        model = User
        fields = ['phone', 'full_name', 'password', 'role']

    def validate_role(self, value):
        if value != 'parent':
            raise serializers.ValidationError("Only parents can register")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)