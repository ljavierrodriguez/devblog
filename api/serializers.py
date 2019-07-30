from .models import User, Post, Portfolio
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField()
    #first_name = serializers.CharField(required=False, default='')
    #last_name = serializers.CharField(required=False, default='')
    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'username', 'password', 'first_name', 'last_name',) # there what you want to initial.


    def create(self, validated_data):
        user = User.objects.create(
            username= validated_data['username'],
            #email = validated_data['email'],
            #first_name = validated_data['first_name'],
            #last_name = validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',)
        #fields = ('__all__')
        exclude = ('password', 'user_permissions', 'groups', 'date_joined', 'is_superuser',)

class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'resume', 'content', 'date', 'image', 'user',)


class PortfolioSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Portfolio
        fields = ('id', 'image', 'skills', 'duration', 'cost', 'url', 'description', 'user',)
