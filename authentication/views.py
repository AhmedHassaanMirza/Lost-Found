from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from .models import ImageData
import os
from datetime import datetime
from django.http import QueryDict
from .apps import FaceRec as model
import pickle5 as pickle
import threading
#from insightface_code.functions import FaceRec as FC
import base64
#with open('my_model.pkl','wb') as file:
 #   pickle.dump(FC(),file)
#my_model=pickle.load('my_model.pkl','r')
def make_update(data_ins):
    my_model=None
    with open('my_model.pkl','rb') as file:
        my_model=pickle.load(file)
    src_feat=my_model.get_feats(data_ins.photo.path)
    try:
        data_ins.feats=base64.b64encode(pickle.dumps(src_feat))
    except:
        print("rasie error1111")
    data_ins.save()
    current_id=data_ins.pk
    all_data=None
    src_img = data_ins.photo.path
    lf=True
    if data_ins.lost_found:
        lf=  False
    all_data=ImageData.objects.filter(lost_found=lf).exclude(id=current_id).exclude(feats=None).all()
    tars=[]
    for i in all_data:
        try:
            tars.append(pickle.loads(base64.b64decode(i.feats)))
        except:
            print("error!")
    matched=None
    try:
        matched=my_model.verify_face(src_feat,tars)
    except:
        print("error raise!")
        matched=None
    if matched !=None :
        mat_obj=all_data[matched]
        data_ins.is_matched = True
        data_ins.matched_id=mat_obj.id
        data_ins.save()
        mat_obj.is_matched=True
        mat_obj.matched_id=current_id
        mat_obj.save()

def index(request):
    params = {
        "logged_in": request.user.is_authenticated
    }
    return render(request, 'index.html', params)


def register(request):

    if request.method == 'POST':

        email = request.POST['email']
        username = request.POST['new_username']
        password = request.POST['new_password']
        first_name = request.POST['new_district_city']
        last_name = request.POST['new_police_station']
        

        if User.objects.filter(username=username).exists():
            params = {
                "success": 0,
                "message": "The email is already in use. If this email is yours, you can try to login"
            }
            return render(request, 'register.html', params)

        user = User.objects.create_user(
            username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        print('user created')
        return redirect('/dashboard')
    else:
        if request.user.is_authenticated:
            return redirect('/dashboard')
        return render(request, 'register.html')

@csrf_exempt
def login(request):

    if request.method == 'POST':
        print(request.POST)
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        role='user'


        if user is not None:
            is_s=User.objects.get(username=username).is_staff
            if(is_s):
                role='admin'
            if (user.is_active):
                auth.login(request, user)
                return redirect(f'/{role}dashboard')
            else:
                messages.info(
                    request, 'This user is not active. Contact Admin!')
                params = {
                    "success": 0,
                    "message": "This user is not active. Contact Admin!"
                }
                return render(request, 'login.html', params)
        else:
            
            params = {
                "success": 0,
                "message": "Email or password is invalid"
            }
            return render(request, 'login.html', params)
    else:
        if request.user.is_authenticated:
            role='user'
            is_s=request.user.is_staff
            if(is_s):
                role='admin'

            
            return redirect(f'/{role}dashboard')
        
        params = {
                "success": 2,
                "message": "Email or password is invalid"
            }
        return render(request, 'login.html',params)
@csrf_exempt
def signout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponse("logoutsuccess")
 
    return render(request, 'login.html')

@login_required(login_url='/login/')
def dashboard(request):
    role="user"
    if request.user.is_staff:
        role="admin"
    params={"name":request.user.username,
    "police_station":request.user.first_name,
    "district_city":request.user.last_name,
    "role":role,
    } 
    if request.method == 'POST':
        return 'Method is not allowed'
    else:
        return render(request, 'dashboard.html',params)
@csrf_exempt
@login_required(login_url='/login/')
def upload_person(request):
    my_model=None
    # if request.method == 'POST':
       
    #             return render(request, 'login.html')
    
    # else :
    # imageIns=ImageData(user="Ahmed",
    #                     person_name=request.POST.get('person_name')
    data_ins=ImageData(user=request.user.username,
                        person_name=request.POST.get('name_person'),
                        police_station=request.POST.get('police_station'),
                        person_contact=request.POST.get('number_contactperson'),
                        GD_case_no=request.POST.get('GD_case_no'),
                        GD_case_date=request.POST.get('GD_case_date'),
                        officer_no=request.POST.get('enrollment_officer_phonenumber'),
                        photo=request.FILES['photo'],
                        upload_date=datetime.now(),
                        lost_found=bool(int(request.POST.get('lost_found'))),
                         
                        )
    data_ins.save()


   # with open('my_model.pkl','rb') as file:
   #     my_model=pickle.load(file)
   # src_feat=my_model.get_feats(data_ins.photo.path)
   # try:
   #     data_ins.feats=base64.b64encode(pickle.dumps(src_feat))
   # except:
   #     print("rasie error1111")
   # data_ins.save()
   # current_id=data_ins.pk
   # all_data=None
   # src_img = data_ins.photo.path
   # lf=True
   # if data_ins.lost_found:
   #     lf=  False
   # all_data=ImageData.objects.filter(lost_found=lf).exclude(id=current_id).exclude(feats=None).all()
   # tars=[]
   # for i in all_data:
   #     try:
   #         tars.append(pickle.loads(base64.b64decode(i.feats)))
   #     except:
   #         print("error!")
   # matched=None
   # try:
   #     matched=my_model.verify_face(src_feat,tars)
   # except:
   #     print("error raise!")
   #     matched=None
   # if matched !=None :
   #     mat_obj=all_data[matched]
   #     data_ins.is_matched = True
   #     data_ins.matched_id=mat_obj.id
   #     data_ins.save()
   #     mat_obj.is_matched=True
   #     mat_obj.matched_id=current_id
   #     mat_obj.save()
    t=threading.Thread(target=make_update,args=[data_ins])
    t.setDaemon(True)
    t.start()
    role="user"
    if request.user.is_staff:
        role="admin"
  
    params={"name":request.user.username,
    "police_station":request.GET.get('police_station'),
    "district_city":request.GET.get('district_city'),
    "role":role}
    return render(request,'dashboard.html', params)   
        
@login_required(login_url='/login/')
def matched_photos(request):
    objs=None
    if request.user.is_staff:
        objs=ImageData.objects.filter(is_matched=True).all()
    else:
        objs=ImageData.objects.filter(user=request.user.username,is_matched=True).all()
    final_objs=[]
    for i in objs:
        obj=ImageData.objects.get(id=i.matched_id)
        final_objs.append([i,obj]) 
    print(len(final_objs))
    role="user"
    if request.user.is_staff:
        role="admin"
    
    params={"name":request.user.username,
    "police_station":request.GET.get('police_station'),
    "district_city":request.GET.get('district_city'),
    "role":role,
    "persons":final_objs}    
    return render(request,'matchedphotos.html', params)
@login_required(login_url='/login/')
def unmatched_photos(request):
    objs=None
    
    if request.user.is_staff:
        objs=ImageData.objects.filter(is_matched=False).all()
    else:
        objs=ImageData.objects.filter(user=request.user.username,is_matched=False).all()
    role="user"
    if request.user.is_staff:
        role="admin"
    params={"name":request.user.username,
    "police_station":request.GET.get('police_station'),
    "district_city":request.GET.get('district_city'),
    "role":role,
    "persons":objs}    
    return render(request,'unmatchedphotos.html', params)
@login_required(login_url='/login/')
@csrf_exempt
def all_photos(request):
    if request.method == "POST":
        my_obj=ImageData.objects.get(upload_date=request.POST.get('upload_date'))
        if my_obj.is_matched:
            matched=ImageData.objects.get(id=my_obj.matched_id)
            matched.is_matched=False
            matched.matched_id=None
            matched.save()
        my_obj.delete()
        
    objs=None
    if request.user.is_staff:
        objs=ImageData.objects.all()
    else:
        objs=ImageData.objects.filter(user=request.user.username).all()
    role="user"
    if request.user.is_staff:
        role="admin"
    params={"name":request.user.username,
    "police_station":request.user.first_name,
    "district_city":request.user.last_name,
    "role":role,
    "persons":objs} 
    print("hellooo",len(objs))   
    return render(request,'allphotos.html', params)
@login_required(login_url='/login/')
def administ(request):
    if not request.user.is_staff:
        return redirect('/useradministration/')
    if request.method == 'POST':
        print("loooooooooook art            herer")
        email = request.POST['email']
        username = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        if User.objects.filter(username=username).exists():
            params = {
                "success": 0,
                "message": "The email is already in use. If this email is yours, you can try to login"
            }
            return render(request, 'register.html', params)

        user = User.objects.create_user(
            username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        print('user created')
        return render(request, 'admindashboard.html')
        # if request.user.is_authenticated:
        #     return redirect('/administration')
    return render(request, 'admindashboard.html')

    params={"name":"none",
    "police_station":request.GET.get('police_station'),
    "district_city":request.GET.get('district_city'),
    "role":"None"}    
    print("look at this user= ",request.user)
    return render(request,'admindashboard.html', params)

@csrf_exempt
def load_users(request):
    if request.method == 'POST':
        username=request.POST['name']
        User.objects.filter(username=username).delete()
        print(User.objects.filter(username=username[0]))
        return HttpResponse("hello")
    users=User.objects.all().exclude(is_staff=True)
       
    objs=ImageData.objects.all().filter(user=request.user.username)
    role="user"
    if request.user.is_staff:
        role="admin"
    params={"name":request.user.username,
    # "police_station":request.GET.get('police_station'),
    # "district_city":request.GET.get('district_city'),
    "role":role,
    "users":users} 
    return render(request,'users.html',params)

@csrf_exempt
def generate(request):
    ##Using Email as Role and
    params={"name":"none",
    "police_station":request.user.first_name,
    "district_city":request.user.last_name,
    "role":request.user.email}  
    if request.method == 'POST':
        print("looook",request.user.password)

        # email = request.POST['new_username']

        username = request.POST['new_username']
        password = request.POST['new_password']
        first_name = request.POST['new_district_city'] #using first_name as new_district_city
        last_name = request.POST['new_police_station'] #using last_name as new_police_station
        email=username ## using as role

        if User.objects.filter(username=username).exists():
            params = {
                "success": 0,
                "message": "The email is already in use. If this email is yours, you can try to login"
            }
            return render(request, 'register.html', params)

        user = User.objects.create_user(
            username=username, password=password, email=email, first_name=first_name, last_name=last_name,)
        user.save()
        print('user created')
      
    return render(request,'admindashboard.html', params)
@csrf_exempt
def changepwd(request):
    put = QueryDict(request.body)
    newpwd = put.get('newpassword')
    print('hellllllllllllo')
    my_user=User.objects.get(username=request.user)
    my_user.set_password(newpwd)
    my_user.save()
    print(User.objects.get(username=request.user))
    return HttpResponse("hello")


    
