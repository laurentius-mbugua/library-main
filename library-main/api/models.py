from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
 
# Book model in the library
class Book(models.Model):
    title = models.CharField(max_length=255) # Stores the title of the book
    author = models.CharField(max_length=255) # Stores the author
    isbn = models.CharField(max_length=13, unique=True) # Stores the book’s unique ISBN
    published_date = models.DateField() # Stores the publication date of the book
    copies_available = models.PositiveIntegerField(default=1) #  how many copies of the book are available for borrowing


    def __str__(self):
        return self.title    # Defines the string representation of the Book when printed  
     

# UserProfile model to extend User model with additional information

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # one-to-one relationship between the UserProfile and Django's built-in User model a One UserProfile with one User
    date_of_membership = models.DateField(auto_now_add=True)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

#  create a UserProfile whenever a new User is created

@receiver(post_save, sender=User) # signal that listens when a User model is saved after save()  
def create_user_profile(sender, instance, created, **kwargs): # it creates a corresponding UserProfile for that User or UserProfile  is updated  
    if created:
        UserProfile.objects.create(user=instance)

# Transaction model that tracks borrowing and returning of books

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions') # ForeignKey defines a many-to-one relationship between the Transaction model and the User model  
    book = models.ForeignKey(Book, on_delete=models.CASCADE) # ForeignKey defines a many-to-one relationship between the Transaction model and a Book model 
    checked_out_date = models.DateTimeField(auto_now_add=True) # DateTimeField  stores the date and time when the transaction  
    returned_date = models.DateTimeField(null=True, blank=True) # DateTimeField stores the date and time when the book is returned

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"




 
   
