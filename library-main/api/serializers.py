from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Transaction
from .models import User, UserProfile

class BookSerializer(serializers.ModelSerializer): # include all the fields from the Book model
    class Meta:
        model = Book
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer): 
    date_of_membership = serializers.DateField(source='userprofile.date_of_membership', read_only=True)
    active_status = serializers.BooleanField(source='userprofile.active_status', default=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_of_membership', 'active_status', 'password']
        extra_kwargs = {'password': {'write_only': True}} # the password field is write-only

    def create(self, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.update_or_create(user=user, defaults=profile_data) # The create method handles the creation of a new User
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()

        UserProfile.objects.update_or_create(user=instance, defaults=profile_data)
        return instance

class TransactionSerializer(serializers.ModelSerializer): # TransactionSerializer is specifically designed to work with the Transaction model
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'user_username', 'book', 'book_title', 'checked_out_date', 'returned_date']
        read_only_fields = ['checked_out_date', 'returned_date']
