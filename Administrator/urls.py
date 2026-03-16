from Administrator import views
from django.urls import path,include
app_name='Admin'

urlpatterns = [
    path('adminregistration/',views.adminregistration,name='adminregistration'),
    path('district/',views.district,name='district'),
    path('category/',views.category,name='category'),
    path('deletedistrict/<int:did>',views.deletedistrict,name='deletedistrict'),
    path('editdistrict/<int:did>',views.editdistrict,name='editdistrict'),
    path('deleteadmin/<int:did>',views.deleteadmin,name='deleteadmin'),
    path('editadmin/<int:did>',views.editadmin,name='editadmin'),
    path('deletecategory/<int:did>',views.deletecategory,name='deletecategory'),
    path('editcategory/<int:did>',views.editcategory,name='editcategory'),
    path('place/',views.place,name='place'),
    path('deleteplace/<int:did>',views.deleteplace,name='deleteplace'),
    path('editplace/<int:did>',views.editplace,name='editplace'),
    path('localplace/',views.localplace,name='localplace'),
    path('deletelocalplace/<int:did>',views.deletelocalplace,name='deletelocalplace'),
    path('editlocalplace/<int:did>',views.editlocalplace,name='editlocalplace'),
    path('workcategory/',views.workcategory,name='workcategory'),
    path('deleteworkcategory/<int:did>',views.deleteworkcategory,name='deleteworkcategory'),
    path('editworkcategory/<int:did>',views.editworkcategory,name='editworkcategory'),
    path('subcategory/',views.subcategory,name='subcategory'),
    path('deletesubcategory/<int:did>',views.deletesubcategory,name='deletesubcategory'),
    path('editsubcategory/<int:did>',views.editsubcategory,name='editsubcategory'),

    path('homepage/',views.homepage,name='homepage'),
    
    path('sellerverification/',views.sellerverification,name='sellerverification'),
    path('electricianverification/',views.electricianverification,name='electricianverification'),
    path('rejectseller/<int:did>',views.rejectseller,name='rejectseller'),  
    path('acceptseller/<int:did>',views.acceptseller,name='acceptseller'),   
    path('viewseller/',views.viewseller,name='viewseller'),
    path('rejectelectrician/<int:did>',views.rejectelectrician,name='rejectelectrician'),  
    path('acceptelectrician/<int:did>',views.acceptelectrician,name='acceptelectrician'),   
    path('viewelectrician/',views.viewelectrician,name='viewelectrician'),
    path('viewuserfeedback/',views.viewuserfeedback,name='viewuserfeedback'),
    path('viewsellerfeedback/',views.viewsellerfeedback,name='viewsellerfeedback'),
    path('bookingreport/',views.bookingreport,name='bookingreport'),
    path('view_complaints/', views.view_complaints, name='view_complaints'),
    path('reply_complaint/<int:complaint_id>/', views.reply_complaint, name='reply_complaint'),
    path('block_electrician/<int:eid>/', views.block_electrician, name='block_electrician'),
    path('unblock_electrician/<int:eid>/', views.unblock_electrician, name='unblock_electrician'),
    path('block_seller/<int:sid>/', views.block_seller, name='block_seller'),
    path('unblock_seller/<int:sid>/', views.unblock_seller, name='unblock_seller'),
    path('logout/',views.logout,name='logout'),
    
]



