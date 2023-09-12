from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile,Post

User = get_user_model()


class AllUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'profilepic', 'is_writer', 'is_admin', 'is_staff', 'is_superuser', 'is_active']
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    # profilepic = serializers.ImageField(required=True)
    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        user = UserProfile.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["email"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        attrs["user"] = user
        return attrs
    


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "email",
            'username',
            'first_name',
            'last_name',
            'is_writer',
            'profilepic'
        ]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        # Check if the user making the request is an admin
        is_admin = self.context['request'].user.is_admin

        if not is_admin:
            # Owner is making the request
            validated_data.pop('is_writer', None)
            validated_data.pop('is_admin', None)
            validated_data.pop('is_staff', None)
            validated_data.pop('is_superuser', None)
              # Remove 'is_writer' from validated_data

        # Update the UserProfile instance with the validated data
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.profilepic = validated_data.get("profilepic", instance.profilepic)
        
        if is_admin:
            instance.is_writer = validated_data.get("is_writer", instance.is_writer)
            
        instance.save()
        return instance

    def delete(self, instance):
        # Delete the UserProfile instance
        instance.delete()



class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_first_name = serializers.CharField(source='author.first_name', read_only=True)
    author_last_name = serializers.CharField(source='author.last_name', read_only=True)
    author_picture = serializers.ImageField(source='author.profilepic', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['author_username', 'author_first_name', 'image', 'author_last_name', 'author_picture', 'image_url', 'id', 'title', 'content', 'created_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()