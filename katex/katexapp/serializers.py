from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import  urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
UserModel = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                    token, created = Token.objects.get_or_create(user=user)
                    data['token'] = token.key
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password" fields.')
        return data

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError(_('Email address must be provided'))
        try:
            user = UserModel.objects.get_by_natural_key(email)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(_('No user with this email address.'))

        # Generate a unique token for the user
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Save the token to the user's reset_token field
        user.reset_token = token
        user.save()

        # Send an email to the user with a link to the password reset page
        # (You will need to implement this yourself)

        attrs['user'] = user
        attrs['token'] = token
        return attrs

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        token = attrs.get('token')

        if not password:
            raise serializers.ValidationError(_('Password must be provided'))
        if not token:
            raise serializers.ValidationError(_('Token must be provided'))

        try:
            uidb64 = self.context.get('uidb64')
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(id=uid)
        except:
            raise serializers.ValidationError(_('Invalid user'))

        if user.reset_token != token:
            raise serializers.ValidationError(_('Invalid token'))

        user.set_password(password)
        user.reset_token = ''
        user.save()

        return attrs


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('author',)

    def create(self, validated_data):
        post = Post.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        return post

class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('author', 'slug', 'created_at', 'updated_at')

class PublishPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('is_published',)

    def update(self, instance, validated_data):
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.save()
        return instance

class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = []
    
    def delete(self):
        self.instance