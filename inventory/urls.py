from django.urls import path
from . views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('dashboard/', dashboard, name='dashboard'),

   
    path("orderplaced/", orderplaced, name = "orderplaced"),
    path("vieworderplaced/<int:pk>", orderplaced_view, name = "view_orderplaced"),
    path("Deleteorderplaced/<int:pk>", delete_orderplaced, name = "delete_orderplaced"),
    path("Updateorderplaced/<int:pk>", update_orderplaced, name = "update_orderplaced"),
    path("searchorderplaced/", searchorderplaced, name = "searchorderplaced"),


    path("Review/", Reviews, name = "Review"),
    path("viewReview/<int:pk>", review_view, name = "view_review"),
    path("DeleteReview/<int:pk>", delete_review, name = "delete_review"),
    path("addReview/", addReviews, name = "addReview"),
    path("UpdateReview/<int:pk>", update_review, name = "update_review"),

    
    path('ordercabin/', ordercabin, name='ordercabin'),
    path('view_cabin_orders/<int:pk>/', view_cabin_orders, name='view_cabin_orders'),
     path('delete_cabin_order/<int:pk>/', delete_cabin_order, name='delete_cabin_order'),
    path('add_cabin_order_with_cabin/', add_cabin_order_with_cabin, name='add_cabin_order_with_cabin'),
    path('add_cabin_order_without_cabin/<int:cabin_pk>/', add_cabin_order_without_cabin, name='add_cabin_order_without_cabin'),

    path('billing/', billing, name='billing'),
    path('billing-summary/', billing_summary, name='billing_summary'),
    path('cabinorder-search/', cabinorder_search, name='cabinorder_search'),

    path("cabin/", cabins, name = "cabin"),
    path('addcabin/', addcabin, name='add_cabin'),
    path('viewcabin/<int:pk>/', cabin_view, name='view_cabin'),
    path('deletecabin/<int:pk>/', delete_cabin, name='delete_cabin'),
    path('updatecabin/<int:pk>/', update_cabin, name='update_cabin'),

    path("Product/", Products, name = "Product"),
    path('viewProduct/<int:pk>/', product_view, name='view_product'),
    path('deleteProduct/<int:pk>/', delete_product, name='delete_product'),
    path('addProduct/', addProduct, name='add_product'),
    path('updateProduct/<int:pk>/', update_product, name='update_product'),
    path("searchproduct/", searchproduct, name = "searchproduct"),

    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

