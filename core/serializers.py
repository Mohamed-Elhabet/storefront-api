# from djoser.serializers import UserCreateSerializer \
#     as BaseUserCreateSerializer
# from rest_framework import serializers


# class UserCreateSerializer(BaseUserCreateSerializer):
#     class Meta(BaseUserCreateSerializer.Meta):
#         fields = ['id', 'username', 'password', 'email',
#                   'first_name', 'last_name']




from djoser.serializers import UserCreateSerializer \
    as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password1', 'password2', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        password1 = attrs.pop('password1')
        password2 = attrs.pop('password2')

        if password1 != password2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        attrs['password'] = password1
        return attrs

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
