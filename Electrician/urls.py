from Electrician import views
from django.urls import path,include
app_name='Electrician'

urlpatterns = [
    path('myprofile/', views.myprofile, name='myprofile'),
    path('work_gallery/', views.work_gallery, name='work_gallery'),
    path('delete_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('delete_work/', views.delete_work, name='delete_work'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('dahomepage/',views.dahomepage,name='dahomepage'),
    
    path('my_bookings/',views.my_bookings,name='my_bookings'),
    path('accept_booking/<int:id>',views.accept_booking,name='accept_booking'),
    path('reject_booking/<int:id>',views.reject_booking,name='reject_booking'),
    path('send_estimate/<int:id>',views.send_estimate,name='send_estimate'),
    path('complete_booking/<int:id>',views.complete_booking,name='complete_booking'),

    path('viewseller/',views.viewseller,name='viewseller'),
    path('ajaxplace/',views.ajaxplace,name='ajaxplace'),
    path('ajaxsellersearch/',views.ajaxsellersearch,name='ajaxsellersearch'),
    path('viewproduct/<int:did>',views.viewproduct,name='viewproduct'),
    path('ajaxsubcategory/',views.ajaxsubcategory,name='ajaxsubcategory'),
    path('ajaxsearch/',views.ajaxsearch,name='ajaxsearch'), 
    path('Addcart/<int:pid>',views.Addcart,name='Addcart'), 
    path('Mycart/',views.Mycart, name='Mycart'),   
    path("DelCart/<int:did>", views.DelCart,name="delcart"),
    path("CartQty/", views.CartQty,name="cartqty"),

    path("productpayment/", views.productpayment,name="productpayment"),
    path('loader/',views.loader, name='loader'),
    path('paymentsuc/',views.paymentsuc, name='paymentsuc'),
    
    path('mybooking/',views.mybooking,name='mybooking'),
    path('viewcartproduct/<int:id>',views.viewcartproduct,name='viewcartproduct'),
    
    path('view_complaints/', views.view_complaints, name='view_complaints'),
    path('reply_complaint/<int:complaint_id>/', views.reply_complaint, name='reply_complaint'),

    path('logout/',views.logout,name='logout'),
]
