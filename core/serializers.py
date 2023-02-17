from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

# custom serializer that extends from djoser to create an account
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['id', 'email','first_name','last_name','username','phone_number','password']