from Seller import views
from django.urls import path,include
app_name='Seller'

urlpatterns = [
    path('myprofile/',views.myprofile,name='myprofile'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('sellerhomepage/',views.sellerhomepage,name='sellerhomepage'),
    path('product/',views.product,name='product'),
    path('deleteproduct/<int:did>',views.deleteproduct,name='deleteproduct'),    
    path('ajaxsubcategory/',views.ajaxsubcategory,name='ajaxsubcategory'),
    path('addstock/<int:id>',views.addstock,name='addstock'), 
    path('viewbooking/',views.viewbooking,name='viewbooking'),
    path('feedback/',views.feedback,name='feedback'),
    path('viewcomplaint/',views.viewcomplaint,name='viewcomplaint'),
    path('replynow/<int:cid>',views.replynow,name='replynow'),
    path('view_complaints/', views.view_complaints, name='view_complaints'),
    path('reply_complaint/<int:complaint_id>/', views.reply_complaint, name='reply_complaint'),
    path("packorder/<int:id>", views.packorder, name="packorder"),
    path("shiporder/<int:id>", views.shiporder, name="shiporder"),
    path("outfordelivery/<int:id>", views.outfordelivery, name="outfordelivery"),
    path("delivered/<int:id>", views.delivered, name="delivered"),
    path('logout/',views.logout,name='logout'),

    path('viewreport/',views.viewreport,name='viewreport'),
    path('pdtchart/',views.pdtchart,name='pdtchart'),

    path('viewelectrician/<int:did>',views.viewelectrician,name='viewelectrician'),
]

