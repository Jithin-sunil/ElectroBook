from Guest import views
from django.urls import path,include
app_name='Guest'

urlpatterns = [
    path('userregistration/',views.userregistration,name='userregistration'),
    path('ajaxplace/',views.ajaxplace,name='ajaxplace'),
    path('ajaxlocalplace/',views.ajaxlocalplace,name='ajaxlocalplace'),
    path('login/',views.login,name='login'),
    path('sellerreg/',views.sellerreg,name='sellerreg'),
    path('Electricianreg/',views.Electricianreg,name='Electricianreg'),
    path('',views.index,name='index'),
    
]

