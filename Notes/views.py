from django.shortcuts import render,redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import*

from datetime import date

# Create your views here.
def about(request):
    return render(request,'about.html')

def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')
def userlogin(request):
    error=""
    if request.method=='POST':
        u=request.POST['emailid']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request,'login.html',d)

def admin_login(request):
    error=""
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}

    return render(request,'admin_login.html',d)


def signup1(request):
    error=""
    if request.method=='POST':
        f=request.POST['firstname']
        l=request.POST['lastname']
        c=request.POST['contact']
        e=request.POST['emailid']
        p=request.POST['password']
        b=request.POST['branch']
        d=request.POST['designation']
        try:
            user=User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user,contact=c,branch=b,designation=d)
            error="no"
        except:
            error="yes"

    d={'error':error}
    return render(request,'signup.html',d)


def admin_home(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    pn=Notes.objects.filter(status="pending").count()
    an=Notes.objects.filter(status="Accept").count()
    rn=Notes.objects.filter(status="Reject").count()
    alln=Notes.objects.all().count()
    d={'pn':pn,'an':an, 'rn':rn, 'alln':alln}


    return render(request,'admin_home.html',d)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    data=Signup.objects.get(user=request.user)
    d={'data':data,'user':user}
    return render(request,'profile.html',d)

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=="POST":
        o=request.POST['old']
        n=request.POST['new']
        c=request.POST['confirm']

        if c==n:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d={'error':error}
    return render (request,'changepassword.html',d)

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    data=Signup.objects.get(user=request.user)
    error=False
    if request.method=="POST":
        f=request.POST['firstname']
        l=request.POST['lastname']
        c=request.POST['contact']
        b=request.POST['branch']
        d=request.POST['designation']
        user.first_name=f
        user.last_name=l
        data.contact=c
        data.branch=b
        data.designation=d
        user.save()
        data.save()
        error=True

    d={'data':data,'user':user,'error':error}
    return render(request,'edit_profile.html',d)


def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    error = ""
    if request.method == 'POST':
        # Fetching data from POST request
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.FILES['notesFile']
        f = request.POST['filetype']
        se = request.POST['semester']
        de = request.POST['description']
        d = request.POST['designation']
        u = User.objects.filter(username=request.user.username).first()

        try:
            # Creating the Notes object
            Notes.objects.create(
                user=u,
                uploadingdate=date.today(),
                branch=b,
                subject=s,
                designation=d,
                semester=se,
                notesFile=n,
                filetype=f,
                description=de,
                status='pending'
            )
            error = "no"
        except Exception as e:
            print(f"Error: {e}")  # Logs the exact error for debugging
            error = "yes"

    # Passing error status to template
    d = {'error': error}
    return render(request, 'upload_notes.html', d)


def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    notes=Notes.objects.filter(user=user)

    d={'notes':notes}
    return render(request,'view_mynotes.html',d)

def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('view_mynotes')


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    users=Signup.objects.all()
    d={'users':users}
    return render(request,'view_users.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user=User.objects.get(id=pid)
    user.delete()
    return redirect('view_users')

def pending_notes(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    notes = Notes.objects.filter(status='pending')
    d = {'notes': notes}
    return render(request, 'pending_notes.html', d)

def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    notes = Notes.objects.filter(status='Accept')
    d = {'notes': notes}
    return render(request, 'accepted_notes.html', d)

def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    notes = Notes.objects.filter(status='Reject')
    d = {'notes': notes}
    return render(request, 'rejected_notes.html', d)


def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    notes = Notes.objects.all()
    d = {'notes': notes}
    return render(request, 'all_notes.html', d)

def assign_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    notes=Notes.objects.get(id=pid)
    error=""
    if request.method == 'POST':
        # Fetching data from POST request
        s = request.POST['status']
        try:
            notes.status = s
            notes.save()
            error="no"

        except:
            error="yes"

    d={'notes':notes,'error':error}
    return render(request,'assign_status.html',d)


def delete_notes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('all_notes')

def viewallnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.filter(status="Accept")
    d = {'notes': notes}
    return render(request, 'viewallnotes.html', d)