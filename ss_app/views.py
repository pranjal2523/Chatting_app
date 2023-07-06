from django.shortcuts import render
from .models import User, Chat, chat_history
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
 # Create your views here.



# User Registration
def register_user(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']
        dob = request.POST['dob']
        phone = request.POST['phone']
        
        if email is None or name is None or password is None:        
            print("empty POST")
            messages.warning(request, "invalid data")
        else:
            if User.objects.filter(email=email).exists():
                print("same mail")
                messages.info(request, "Email already registered !")
            else:
                user = User.objects.create_user(phone_number=phone, password=password, name=name, email=email, gender=gender, dob=dob)
                user.save()
                messages.success(request, "Account created succesfully")
                return redirect('login_user')
            
    today = timezone.now().strftime("%Y-%m-%d")
    return render(request, 'register.html', {'today': today})

# User Login
def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            request.session['email'] = user.email
            login(request, user)
            user.is_available = True
            user.save()
            #print("login successful")
            return redirect('chat')
        else:
            messages.error(request, "Invalid Credential")
            return render(request, 'login.html')

    return render(request, 'login.html')


def LogoutView(request):
    user_email = request.session['email']
    user = User.objects.get(email=user_email)
    user.is_available = False
    user.save()
    request.session['email'] = ''
    request.session['chat_id'] = ''
    messages.warning(request, "Logged out successfully ")
    logout(request)
    return redirect('login_user')

def chat(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_email = request.session['email']
    user = User.objects.get(email=user_email)
    users = User.objects.exclude(id=request.user.id)
#    chats = Chat.objects.filter(receiver=request.user)
    return render(request, 'chat.html', {'users': users, 'username':user.name})

def  create_chat(request, recieveremail):
    sender = request.user
    reciever = User.objects.get(email= recieveremail)
    try:
        ch = chat_history.objects.get(sender=reciever, reciever=sender)
    except:
        ch = chat_history.objects.get_or_create(sender=sender, reciever=reciever)[0]
    
    #ch = ch[0]
    chat_id = ch.pk
    request.session['chat_id'] = chat_id
    return redirect('chatview', chat_id)


def  chatview(request,chat_id):
   
    if request.method == 'GET':

      users = User.objects.exclude(id=request.user.id)
      request.session['chat_id'] = chat_id
      print(chat_id)
      chat_history_obj = chat_history.objects.get(id=chat_id)
      c = Chat.objects.filter(chat_history_id=chat_id)

      return render(request,'chat.html', {"users":users, "consultation":chat_history_obj, 'chat': c, 'user':request.user})



def post(request):
    if request.method == "POST":
        print("function callled")
        msg = request.POST['msgbox']

        chat_id = request.session['chat_id'] 
        chat_history_obj = chat_history.objects.get(id=chat_id)

        c = Chat(chat_history_id=chat_history_obj,sender_id=request.user, message=msg)

        #msg = c.user.username+": "+msg
        print("no error", msg)
        if msg != '':            
            c.save()
            #print("msg saved"+ msg )
            return redirect('chatview', chat_id)
    else:
        print("error in Post")
        return HttpResponse('Request must be POST.')
    
