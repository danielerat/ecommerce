from djoser.serializers import UserSerializer as BaseUserSerializer,UserCreateSerializer as BaseUserCreateSerializer

# custom serializer that extends from djoser to create an account
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['id', 'email','first_name','last_name','username','phone_number','password']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['id', 'username','first_name','last_name','email','phone_number']
