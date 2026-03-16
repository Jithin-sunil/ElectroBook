from django.shortcuts import render, redirect
from Guest.models import *
from Administrator.models import *


# Create your views here.
def userregistration(request):
    District=tbl_district.objects.all()
    place=tbl_place.objects.all()
    if request.method=='POST':
        user_name=request.POST.get("txt_regname")
        user_email=request.POST.get("txt_regemail")
        user_contact=request.POST.get("txt_regcontact")
        user_address=request.POST.get("txt_regaddress")
        place_id=tbl_place.objects.get(id=request.POST.get("place"))
        user_photo=request.FILES.get('txt_regphoto')
        user_password=request.POST.get("txt_password")  
        tbl_user.objects.create(user_name=user_name,user_email=user_email,user_contact=user_contact,user_address=user_address,place=place_id,user_photo=user_photo,user_password=user_password,)
        return redirect('Guest:userregistration')
    else:
        return render(request,'Guest/UserRegistration.html',{'District':District,'place':place})


def ajaxplace(request):
    place=tbl_place.objects.filter(district=request.GET.get('did'))
    return render(request,'Guest/ajaxplace.html',{'place':place})

def ajaxlocalplace(request):
    local_place=tbl_local_place.objects.filter(place=request.GET.get('pid'))
    return render(request,'Guest/ajaxlocalplace.html',{'local_place':local_place})


def login(request):
    if request.method=='POST':
        admincount=tbl_admin.objects.filter(admin_email=request.POST.get('txt_uname'),admin_password=request.POST.get('txt_apassword')).count()
        usercount=tbl_user.objects.filter(user_email=request.POST.get('txt_uname'),user_password=request.POST.get('txt_apassword')).count()
        sellercount=tbl_seller.objects.filter(seller_email=request.POST.get('txt_uname'),seller_password=request.POST.get('txt_apassword')).count()
        dacount=tbl_electrician.objects.filter(electrician_email=request.POST.get('txt_uname'),electrician_password=request.POST.get('txt_apassword')).count()
        
        if admincount > 0:
            admin=tbl_admin.objects.get(admin_email=request.POST.get('txt_uname'),admin_password=request.POST.get('txt_apassword'))
            request.session['aid']=admin.id
            return redirect('Admin:homepage')
        elif usercount > 0:
            user=tbl_user.objects.get(user_email=request.POST.get('txt_uname'),user_password=request.POST.get('txt_apassword'))
            request.session['uid']=user.id
            return redirect('User:userhomepage')
        elif sellercount > 0:
            seller=tbl_seller.objects.get(seller_email=request.POST.get('txt_uname'),seller_password=request.POST.get('txt_apassword'))
            request.session['sid']=seller.id
            if seller.seller_status==0:
                return render(request,'Guest/Login.html',{'msg':'pending'})
            elif seller.seller_status==2:
                return render(request,'Guest/Login.html',{'msg':'blocked'})
            else:
                return redirect('Seller:sellerhomepage')
        elif dacount > 0:
            delivery=tbl_electrician.objects.get(electrician_email=request.POST.get('txt_uname'),electrician_password=request.POST.get('txt_apassword'))
            request.session['did']=delivery.id
            if delivery.local_place:
                request.session['local_place']=delivery.local_place.id
            if delivery.electrician_status==0:
                return render(request,'Guest/Login.html',{'msg':'pending'})
            elif delivery.electrician_status==2:
                return render(request,'Guest/Login.html',{'msg':'blocked'})
            else:
                return redirect('Electrician:dahomepage')
        else:
            return render(request,'Guest/Login.html',{'msg':'invalid'})
    else:
        return render(request,'Guest/Login.html')
        

            


def sellerreg(request):
    District=tbl_district.objects.all()
    place=tbl_place.objects.all()
    if request.method=='POST':
        seller_name=request.POST.get("txt_regname")
        seller_email=request.POST.get("txt_regemail")
        seller_contact=request.POST.get("txt_regcontact")
        seller_address=request.POST.get("txt_regaddress")
        place_id=tbl_place.objects.get(id=request.POST.get("place"))
        seller_logo=request.FILES.get('txt_logo')
        seller_proof=request.FILES.get('txt_proof')
        seller_password=request.POST.get("txt_password")  
        tbl_seller.objects.create(seller_name=seller_name,seller_email=seller_email,seller_contact=seller_contact,seller_address=seller_address,place=place_id,seller_logo=seller_logo,seller_proof=seller_proof,seller_password=seller_password,)
        return redirect('Guest:sellerreg')
    else:
        return render(request,'Guest/Seller.html',{'District':District,'place':place})


def Electricianreg(request):
    District=tbl_district.objects.all()
    place=tbl_place.objects.all()
    category=tbl_work_category.objects.all()
    if request.method=='POST':
        electrician_name=request.POST.get("txt_regname")
        electrician_email=request.POST.get("txt_regemail")
        electrician_contact=request.POST.get("txt_regcontact")
        electrician_address=request.POST.get("txt_regaddress")
        local_place_id=tbl_local_place.objects.get(id=request.POST.get("local_place"))
        work_category_id=tbl_work_category.objects.get(id=request.POST.get("category"))
        electrician_photo=request.FILES.get('txt_photo')
        electrician_aadhar=request.FILES.get('txt_aadhar')
        electrician_pcc=request.FILES.get('txt_pcc')
        electrician_password=request.POST.get("txt_password")  
        tbl_electrician.objects.create(electrician_name=electrician_name,electrician_email=electrician_email,electrician_contact=electrician_contact,electrician_address=electrician_address,local_place=local_place_id,work_category=work_category_id,electrician_photo=electrician_photo,electrician_aadhar=electrician_aadhar,electrician_pcc=electrician_pcc,electrician_password=electrician_password)
        return redirect('Guest:Electricianreg')
    else:
        return render(request,'Guest/Electrician.html',{'District':District,'place':place, 'WorkCategory':category})


def index(request):
    return render(request,"Guest/index.html")