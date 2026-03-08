from User import views
from django.urls import path,include
app_name='User'

urlpatterns = [
    path('userhomepage/',views.userhomepage,name='userhomepage'),
    path('myprofile/',views.myprofile,name='myprofile'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('complaint/<int:id>/<int:complaint_type>',views.complaint,name='complaint'),
    path('complaint/<int:id>',views.complaint,name='complaint_product'),
    path('complaint_electrician/<int:id>',views.complaint,{'complaint_type':2},name='complaint_electrician'),
    path('complaint_site/',views.complaint,{'complaint_type':3},name='complaint_site'),
    path('viewcomplaint/',views.viewcomplaint,name='viewcomplaint'), 
    path('viewseller/', views.viewseller, name='viewseller'),
    path('viewelectricians/', views.viewelectricians, name='viewelectricians'),
    path('electrician_rating/<int:mid>', views.electrician_rating, name='electrician_rating'),
    path('view_electrician_gallery/<int:did>', views.view_electrician_gallery, name='view_electrician_gallery'),
    path('ajax_electrician_star/', views.ajax_electrician_star, name='ajax_electrician_star'),
    path('ajaxelectriciansearch/', views.ajaxelectriciansearch, name='ajaxelectriciansearch'),
    path('bookelectrician/<int:did>',views.bookelectrician,name='bookelectrician'),
    path('myworkbookings/',views.myworkbookings,name='myworkbookings'),
    path('pay_estimate/<int:id>',views.pay_estimate,name='pay_estimate'),
    path('viewproduct/<int:did>',views.viewproduct,name='viewproduct'), 
    path('Addcart/<int:pid>',views.Addcart,name='Addcart'), 
    path('Mycart/',views.Mycart, name='Mycart'),   
    path("DelCart/<int:did>", views.DelCart,name="delcart"),
    path("CartQty/", views.CartQty,name="cartqty"),

    path("productpayment/", views.productpayment,name="productpayment"),
    path('loader/',views.loader, name='loader'),
    path('paymentsuc/',views.paymentsuc, name='paymentsuc'),

    path('feedback/',views.feedback,name='feedback'),
    path('mybooking/',views.mybooking,name='mybooking'),
    path('viewcartproduct/<int:id>',views.viewcartproduct,name='viewcartproduct'),
    path("viewcomplaint/", views.viewcomplaint,name="viewcomplaint"),
  
    path('rating/<int:mid>',views.rating,name="rating"),  
    path('ajaxstar/',views.ajaxstar,name="ajaxstar"),
    path('starrating/',views.starrating,name="starrating"),

    path('ajaxsubcategory/',views.ajaxsubcategory,name='ajaxsubcategory'),
    path('ajaxsearch/',views.ajaxsearch,name='ajaxsearch'),
    path('ajaxsellersearch/',views.ajaxsellersearch,name='ajaxsellersearch'),
    path('logout/',views.logout,name='logout'),
    path('ajaxplace/',views.ajaxplace,name='ajaxplace'),
    path('ajaxlocalplace/',views.ajaxlocalplace,name='ajaxlocalplace'),
    
    

]



