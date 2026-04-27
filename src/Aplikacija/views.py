#* Marko Dasic 2022/0731
#* Pavle Kotlajic
#* Vladana Babic 2021/0546
#* Nina Bucalo 2021/0482

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import IntegrityError
from .models import *
from .forms import *
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import uuid


from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

from datetime import datetime

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

from datetime import datetime


from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

from datetime import datetime
import random
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
User = get_user_model()





def homePage(request):
    """
    **home page**
    """
    return render(request, 'home.html')


def registerPage(request):
    """

    **Register page**
    Displays a set of fields which user needs to write into to make a registration to the app.

    """
    if request.user.is_authenticated:
        return redirect('main')

    form = MyUserCreationForm()
    hobbies = Hobby.objects.all()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)      # So we can save some aditional settings
            user.username = user.username.lower()
            user.save()
            user.iduser = str(user.id)
            user.save()
            user.hobbies.set(form.cleaned_data['hobbies'])
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'There was an error with registration')

    return render(request, 'register.html', {'form': form})


def loginPage(request):
    """

    **Login page**
    Displays a username and password field (login form). User needs to fill those out to login.

    **Template** 
    :template: '../login.html'

    After a user is logged in, it redirects the user to the main page.

    """
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('profile_admin')
            else:
                return redirect('main')
        else:
            messages.error(request, 'Username or password is incorrect')
        
    context = {}
    return render(request, 'login.html', context)



def logoutPage(request):
    """

    *Logout page*

    """
    logout(request)
    return redirect('home')


# User Profile
@login_required(login_url='login')
def profile_userPage(request, pk):
    """

    Displays an individual user profile page

    **Template** 
    :template: '../profile_user.html'

    """
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'profile_user.html', context)


@login_required(login_url='login')
def update_userPage(request):
    user = request.user
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'update_user.html', {'form': form})


@login_required(login_url='login')
def add_rating(request, user_id):
    """

    **Rate a user view**

    should add a restrict for rating <=5 || <=10 ? 

    **Template** 
    :template: '../add_rating.html'

    """
    rated_user = get_object_or_404(User, pk=user_id)
    try:
        rating = Rating.objects.get(user=rated_user, userR=request.user)
        # If a rating exists, populate the form with its instance for editing
        form = RatingForm(request.POST or None, instance=rating)
    except Rating.DoesNotExist:
        rating = None
        form = RatingForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            new_rating = form.save(commit=False)
            if request.user != rated_user:
                new_rating.user = rated_user
                new_rating.userR = request.user
                new_rating.save()
                if rating:  # If rating already existed, it's updated
                    messages.success(request, "Rating updated successfully.")
                else:
                    messages.success(request, "Rating added successfully.")
                return redirect('profile_user', pk=rated_user.pk)
            else:
                messages.error(request, "You cannot rate yourself.")
        else:
            messages.error(request, "Invalid form submission.")
    return render(request, 'add_rating.html', {'form': form, 'user': rated_user})



@login_required(login_url='login')
def profile_adminPage(request):
    """
    
    **Admin page**

    Admin uses this view to ban some users based on reports.
    
    """
    reports = Report.objects.all()
    return render(request, 'profile_admin.html', {'reports': reports})



@login_required(login_url='login',)
def admin_banPage(request,user_id):
    korisnik = User.objects.get(pk=user_id)
    return render(request, 'admin_ban.html', {'korisnik': korisnik})


def getreports(request):
    reports = Report.objects.all()
    return render(request, 'profile_admin.html', {'reports': reports})



def ban_user(request, user_id):
    """

    **A view used by admin to ban users**

    """
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        if 'banovanje' in request.POST:
            user.is_suspended = True
            user.suspended_time = (timezone.now() + timedelta(weeks=1)).strftime('%Y-%m-%d %H:%M:%S')
            user.save()
            
            # Create new suspension
            Suspension.objects.create(

                idsus=str(uuid.uuid4())[:30],
                date=timezone.now().strftime('%Y-%m-%d'),
                time=timezone.now().strftime('%H:%M:%S'),
                idadmin=request.user,
                iduser=user
            )

            return redirect('home') 

    return render(request, 'ban_user_template.html', {'korisnik': user})




@login_required(login_url='login')
def mainPage(request):
    """
    
    **Main page**
    Since the code below incorporates machine learning logic, detailed explanations are provided in the comments.
    **Template**

    :template:`../main.html`

    """
    current_user = request.user
    current_user_gender = current_user.gender
    opposite_gender = not current_user_gender

    # Get the hobbies of the current user
    current_user_hobbies = current_user.hobbies.all()
    current_user_hobby_ids = list(current_user_hobbies.values_list('idhobby', flat=True))

    # Get all users of the opposite gender who are not superusers
    users = User.objects.exclude(id=current_user.id).filter(gender=opposite_gender, is_superuser=False)

    if current_user_hobbies.exists() and users.exists():
        # Create feature vectors for users based on their hobbies
        user_feature_vectors = []
        valid_users = []

        for user in users:
            user_hobbies = user.hobbies.all()
            user_hobby_ids = list(user_hobbies.values_list('idhobby', flat=True))
            if user_hobby_ids:  # Only consider users who have hobbies
                user_feature_vector = [1 if idhobby in user_hobby_ids else 0 for idhobby in current_user_hobby_ids]
                user_feature_vectors.append(user_feature_vector)
                valid_users.append(user)

        if user_feature_vectors:
            # Convert to numpy array for compatibility with sklearn
            user_feature_vectors = np.array(user_feature_vectors)

            # If there are fewer users than k, set k to the number of users
            k = min(5, len(valid_users))

            # Initialize KNN model with appropriate parameters (e.g., k value and distance metric)
            knn_model = NearestNeighbors(n_neighbors=k, metric='jaccard')
            knn_model.fit(user_feature_vectors)

            # Create feature vector for the current user
            current_user_feature_vector = [1] * len(current_user_hobby_ids)  # Current user has all the hobbies listed in current_user_hobby_ids

            # Find the k nearest neighbors for the current user
            distances, neighbor_indices = knn_model.kneighbors([current_user_feature_vector])

            neighbor_indices_list = neighbor_indices[0].tolist()

            # Sort users based on their similarity to the current user
            users = [valid_users[index] for index in neighbor_indices_list]
        else:
            users = users = User.objects.exclude(id=current_user.id).filter(gender=opposite_gender, is_superuser=False)
    else:
        users = users = User.objects.exclude(id=current_user.id).filter(gender=opposite_gender, is_superuser=False)
        # ako user nema nijedan hobi nece mu se prikazati prazna lista, vec redom po id sortirani korisnici

    return render(request, 'main.html', {'users': users})
    


# Chats page
@login_required(login_url='login')
def chatsPage(request):
    current_user = request.user
    chats = Chats.objects.filter(Q(iduser1=current_user) | Q(iduser2=current_user))

    chat_data = []
    for chat in chats:
        last_message = Message.objects.filter(
            Q(iduser1=chat.iduser1, iduser2=chat.iduser2) | Q(iduser1=chat.iduser2, iduser2=chat.iduser1)
        ).order_by('-date', '-time').first()
        
        chat_data.append({
            'chat': chat,
            'last_message': last_message
        })

    return render(request, 'chats.html', {'chat_data': chat_data})

@login_required(login_url='login')
def chatPage(request, pk):
    recipient = get_object_or_404(User, pk=pk)
    current_user = request.user

    # Get or create chat between current user and recipient
    chat = Chats.get_chat(current_user, recipient)
    messages = Message.objects.filter(
        iduser1__in=[current_user, recipient],
        iduser2__in=[current_user, recipient]
    ).order_by('date')

    if request.method == 'POST':
        text = request.POST.get('message')
        if text:
            message_id = str(uuid.uuid4())
            time_now = datetime.now().strftime("%H:%M")
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create and save the new message
            Message.objects.create(
                idmsg=message_id,
                iduser1=current_user,
                iduser2=recipient,
                time=time_now,
                date=date_now,
                text=text
            )
            return redirect('chat', pk=pk)

    context = {
        'recipient': recipient,
        'messages': messages,
    }
    return render(request, 'chat.html', context)

@login_required(login_url='login')
def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        message_text = request.POST.get('message_text')
        if recipient_id and message_text:
            current_user = request.user
            recipient_user = get_object_or_404(User, pk=recipient_id)
            
            # Provera postojanja chata između korisnika
            chat = Chats.objects.filter(
                Q(iduser1=current_user, iduser2=recipient_user) | 
                Q(iduser1=recipient_user, iduser2=current_user)
            ).first()
            
            if not chat:
                chat = Chats.objects.create(iduser1=current_user, iduser2=recipient_user, idchat=f"{current_user.id}-{recipient_user.id}")

            # Generisanje random broja za idmsg
            idmsg = random.randint(100000, 999999)
            # Dodela trenutnog vremena bez sekundi
            current_datee = timezone.now().strftime('%d.%m.%Y')
            current_time = timezone.now().strftime('%H:%M')
            Message.objects.create(idmsg=idmsg, iduser1=current_user, iduser2=recipient_user, text=message_text, time=current_time, date=current_datee)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def submit_rating(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        rating_value = request.POST.get('rating')
        if recipient_id and rating_value:
            recipient_user = User.objects.get(id=recipient_id)
            rating, created = Rating.objects.update_or_create(
                user=recipient_user,
                defaults={'rating': rating_value}
            )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def redirect_to_chat(request, user_id):
    # Preusmeravanje na chat stranicu sa izabranim ID-om korisnika
    return redirect('chat', chat_id=user_id)



@login_required
def paymentPage(request):
    """
    
        Payment option, if a user makes a payment he becomes a premium user

        **Template**
        :template:`../payment.html`
    
    """
    return render(request, 'payment.html')

@login_required
def update_premium_flag(request):
    """
    
        If a user clicks "make a payment" button on payment page, it updates the premium flag.

        No template for this view.
    
    """
    if request.method == 'POST':
        # Update the is_premium flag for the current user
        request.user.is_premium = True
        request.user.save()
        return JsonResponse({'message': 'Payment successful!'})
    else:
        return JsonResponse({'error': 'Invalid request method!'}, status=400)



@login_required(login_url='login')
def deletePage(request):

    """

    Delete your user profile.

    **Template**
        :template:`../delete.html`

    """
    return render(request, 'delete.html')



@login_required(login_url='login')
def edit_profilePage(request):
    """

    edit your user profile.

    **Template**
        :template:`../edit_profile.html`

    """

    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    form = MyUserCreationForm(instance=user)
    hobbies = Hobby.objects.all()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            user.hobbies.set(form.cleaned_data['hobbies'])
            messages.success(request, 'Profile updated successfully')
            return redirect('main')
        else:
            errors = form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return render(request, 'edit_profile.html', {'form': form, 'hobbies': hobbies})


@login_required(login_url='login')
def reportPage(request, pk):
    """

    Users can report other users for inappropriate behaviour.

    **Template**

    :template:`../report.html`


    """
    reported_user = get_object_or_404(User, id=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            try:
                report = form.save(commit=False)
                report.iduser1 = request.user

                if request.user != reported_user:
                    report.iduser2 = reported_user
                    report.save()
                    return redirect('profile_user', pk=reported_user.id)
                else:
                    messages.error(request, "You cannot make a report on yourself.")
            except IntegrityError:
                messages.error(request, "You've already made a report on this user.")
    else:
        form = ReportForm()
    return render(request, 'report.html', {'form': form, 'user': reported_user})



@login_required(login_url='login')
def invitePage(request):
    """

    Invite you friend to join the app.

    **Template**
    :template:`../invite.html`


    """
    return render(request, 'invite.html')


def delete_user(request, user_id):
    """

    A view which deletes a user from the database based on the "delete profile" button click on the delete template.

    """
    user = get_object_or_404(User, pk=user_id)

    
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to delete this user!")
        return redirect('home')
    
    try:
        Report.objects.filter(iduser1=user).delete()
        Report.objects.filter(iduser2=user).delete()


        Message.objects.filter(iduser1=user).delete()
        Message.objects.filter(iduser2=user).delete()


        Payment.objects.filter(iduser=user).delete()


        Suspension.objects.filter(idadmin=user).delete()
        Suspension.objects.filter(iduser=user).delete()

  
        Chats.objects.filter(iduser=user).delete()


        user.delete()
        

        messages.success(request, "Deleted successfully.")
    
    except IntegrityError as e:
        messages.error(request, f"Error while deleting the user : {str(e)}")
        return redirect('home')
    
    return redirect('home')
