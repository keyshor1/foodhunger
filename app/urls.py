
from django.urls import path
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm, CustomOrdersForm
from app.views import (
    CustomerRegistrationView, CustomerLoginView
)


urlpatterns = [
    path('', views.home, name='home'),
    # path('home/', views.home, name='home'),
    path('about/', views.about,name='about'),
    path('morecategory/', views.morecategory,name='morecategory'),
    path('customorders/', views.customorders,name='customorders'),
    path('dishes/', views.dishes,name='dishes'),
    path('category/<slug:val>', views.CategoryView.as_view(),name='category'),
    path('category-title/<val>', views.CategoryTitle.as_view(),name='category-title'),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(),name='product-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(),name='updateAddress'),
    path('orders/', views.orders, name='orders'),
    path('orderscustom/', views.orderscustom, name='orderscustom'),


    # cart section
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    path('khalti/payment',views.khaltipayment,name='khaltipayment'),

    path('search/', views.search,name='search'),
    path('reviewdone/', views.Review_rate,name='reviewdone'),
    path('reviews/', views.reviews,name='reviews'),
    path("viewreview/<int:pk>", views.viewreview, name = "viewreview"),


    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    # path('pluswishlist/', views.plus_wishlist),
    # path('minuswishlist/', views.minus_wishlist),



    # login authentication
    path('registration/', CustomerRegistrationView.as_view(), name='customerregistration'),
    path('token/', views.token_send, name="token_send"),
    path('success/', views.success, name="success"),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('error/', views.error_page, name="error"),
    # path('accounts/login/', CustomerLoginView.as_view(), name='login'),
    # path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Food Hunger"
admin.site.site_title = "Food Hunger"
admin.site.site_index_title = "Welcome to Food Hunger kishor"

