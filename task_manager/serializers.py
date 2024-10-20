from rest_framework import serializers
from .models import Task
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task objects.
    
    This serializer translates Task instances into JSON format and
    provides validation for task data.
    """

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'completed_at']
        read_only_fields = ('user', 'completed_at')

    # Validation
    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value
    
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model objects.
    
    This serializer handles the conversion of User instances to JSON
    and includes validation and user-creation logic.
    """
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    # create_user creates User instance & handles password hashing
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    