#* Marko Dasic 2022/0731
#* Vladana Babic 2021/0546
#* Nina Bucalo 2021/0482
#* Pavle Kotlajic 2021/0596

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Stores all the data for a user, id, username, first_name, last_name are all inherited from AbstractUser.
    Related to model Hobby.
    """
    is_admin = models.BooleanField(blank=False, null=True, default=False)
    iduser = models.CharField(db_column='iduser', max_length=30, default='NoIdUser', null=True)
    idadmin = models.CharField(db_column='idadmin', max_length=30, default='NoIdAdmin', null=True)
    picture = models.ImageField(null=True, default="default_avatar.jpg")
    email = models.CharField(max_length=30, unique=True, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.BooleanField(default=True, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_premium = models.BooleanField(blank=False, null=True, default=False)
    premium_time = models.CharField(max_length=30, blank=True, null=True)
    is_suspended = models.BooleanField(blank=False, null=True, default=False)
    suspended_time = models.CharField(max_length=30, blank=True, null=True)
    hobbies = models.ManyToManyField('Hobby', related_name='users', blank=True)

    @property
    def average_rating(self):
        """
        Calculates the average rating for the user
        """
        ratings_received = self.ratings_received.all()
        if ratings_received.exists():
            total_rating = sum([rating.rating for rating in ratings_received])
            return total_rating / ratings_received.count()
        return 0

    class Meta:
        managed = True
        db_table = 'User'



class Rating(models.Model):
    """
    Stores ratings for the users of database. Related to User model. There is a primary keey id inherited from models.Model, 
    but a restriction regarding 2 exact same pairs of user, userR existing in our database exists.
    Rating goes from 1 to 5.
    """
    user = models.ForeignKey(User, related_name='ratings_received', on_delete=models.CASCADE)
    userR = models.ForeignKey(User, related_name='ratings_given', on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rating {self.rating} for {self.user.username}"



class Hobby(models.Model):
    """
    Stores all the hobbies a user can choose from a list. Not related to any other models.
    """
    idhobby = models.CharField(db_column='idhobby', primary_key=True, max_length=30)
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Hobby'


class Message(models.Model):
    """
    Stores all the messages that exist. Related to two different users.
    """
    idmsg = models.CharField(db_column='idmsg', primary_key=True, max_length=36)  # Promenjena dužina na 36
    iduser1 = models.ForeignKey('User', models.DO_NOTHING, db_column='iduser1', related_name='sent_messages')
    iduser2 = models.ForeignKey('User', models.DO_NOTHING, db_column='iduser2', related_name='received_messages')
    time = models.CharField(max_length=30, blank=True, null=True)
    date = models.CharField(max_length=30, blank=True, null=True)
    text = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Message'
        unique_together = (('iduser1', 'iduser2', 'idmsg'),)




class Chats(models.Model):
    """
    Stores all the conversations (chats) in the database. Doesn't store any text messages, only the information about who chatted with whom.
    Like models.Message, it is related to two different users.
    """
    iduser1 = models.ForeignKey('User', models.DO_NOTHING, db_column='iduser1', related_name='chat1')
    iduser2 = models.ForeignKey('User', models.DO_NOTHING, db_column='iduser2', related_name='chat2')
    idchat = models.CharField(db_column='idchat', max_length=30)

    class Meta:
        managed = True
        db_table = 'Chats'
        unique_together = (('iduser1', 'iduser2', 'idchat'),)
    
    def __str__(self):
        return self.idchat

    @classmethod
    def get_chat(cls, user1, user2):
        """
        A method used for creating a new chat or getting an existing one.
        """
        try:
            chat = cls.objects.get(iduser1=user1, iduser2=user2)
        except cls.DoesNotExist:
            try:
                chat = cls.objects.get(iduser1=user2, iduser2=user1)
            except cls.DoesNotExist:
                idchat = f"{user1.id}-{user2.id}"
                chat = cls.objects.create(iduser1=user1, iduser2=user2, idchat=idchat)
        return chat



class Payment(models.Model):
    """
    Stores payment by different users. Each row is related to a user. A date for each payment is known.
    """
    iduser = models.ForeignKey('User', models.DO_NOTHING, db_column='iduser', blank=True, null=True)
    idpay = models.CharField(db_column='idpay', primary_key=True, max_length=30)
    date = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Payment'



class Report(models.Model):
    """
    Stores the reports made by users regarding other users. Related to two different users (it isn't possible to make a report on yourself).
    Report contains a date, time, and a reason for the report.
    """
    iduser1 = models.ForeignKey('User', models.DO_NOTHING, db_column='iduser1', related_name='reports_made')
    iduser2 = models.ForeignKey('User', models.DO_NOTHING, db_column='iduser2', related_name='reports_received')
    idrep = models.CharField(db_column='idrep', max_length=30)
    date = models.CharField(max_length=30, blank=True, null=True)
    time = models.CharField(max_length=30, blank=True, null=True)
    reason = models.CharField(max_length = 150, blank = True, null=True)

    class Meta:
        managed = True
        db_table = 'Report'
        unique_together = (('iduser1', 'iduser2', 'idrep'),)



class Suspension(models.Model):
    """
    
    Stores suspensions of different users. This table is important for the admin only. Related to the admin which suspended the user and the suspended user.

    """
    date = models.CharField(max_length=30, blank=True, null=True)
    time = models.CharField(max_length=30, blank=True, null=True)
    idsus = models.CharField(db_column='idsus', primary_key=True, max_length=30)
    idadmin = models.ForeignKey('User', models.DO_NOTHING, db_column='idadmin', related_name='admin_who_suspended', blank=True, null=True)
    iduser = models.ForeignKey('User', models.DO_NOTHING, db_column='iduser', related_name='user_who_recived_suspension', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Suspension'
