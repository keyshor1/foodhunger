from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views import View
import requests
from . models import Cart, Custom_Orders, Customer, OrderPlaced, Product, Review, Profile
from . forms import CustomerProfileForm, CustomerRegistrationForm, CustomOrdersForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import HttpResponse

from django.core.exceptions import ValidationError

import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm




def home(request):
    try:
        reviews = Review.objects.filter(Q(user=request.user) | Q(status='accepted'))
        biryani_products = Product.objects.filter(category='BF')
        breakfast_products = Product.objects.filter(category='BF')
        lunch_products = Product.objects.filter(category='LH')
        dinner_products = Product.objects.filter(category='DN')
        dessert_products = Product.objects.filter(category='DT')
        drinks_products = Product.objects.filter(category='DR')
        platter_products = Product.objects.filter(category='PT')
        fast_food_products = Product.objects.filter(category='FF')
        popular_dishes_products = Product.objects.filter(category='PD')
        new_arrivals_products = Product.objects.filter(category='NA')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, "app/home.html", locals())
    except:
        return render(request, 'app/home.html', {'error': 'An error occurred'})


def customorders(request):
    category_choice = "NA"  # or any other value from the CATEGORY_CHOICES tuple
    newarrivals_products = Product.objects.filter(category=category_choice)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CustomOrdersForm(request.POST, request.FILES)
            if form.is_valid():
                user = request.user
                photo = form.cleaned_data['photo']
                custom_order = form.save(commit=False)
                custom_order.user = user
                custom_order.photo = photo
                custom_order.custom_status = 'Pending'
                custom_order.save()
                # Retrieve the latest order placed by the user
                order = Custom_Orders.objects.filter(user=user).latest('date')

                # Check the order status
                status = order.custom_status
                if status == 'Pending':
                    subject = 'Order Confirmation'
                    message = f"Dear {user.username}, your customorder has been sent to food hunger check your site to see the status of the order"
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)   
                return redirect('orderscustom')
        else:
            form = CustomOrdersForm()
        context = {'form': form, 'newarrivals_products': newarrivals_products}
        return render(request, "app/customorders.html", context)
    else:
        return redirect('orders')


def orderscustom(request):
    orders_custom = Custom_Orders.objects.filter(user=request.user)
    return render(request, 'app/orderscustom.html', locals())


def dishes(request):
    biryani_products = Product.objects.filter(category='BF')
    breakfast_products = Product.objects.filter(category='BF')
    lunch_products = Product.objects.filter(category='LH')
    dinner_products = Product.objects.filter(category='DN')
    dessert_products = Product.objects.filter(category='DT')
    drinks_products = Product.objects.filter(category='DR')
    platter_products = Product.objects.filter(category='PT')
    fast_food_products = Product.objects.filter(category='FF')
    popular_dishes_products = Product.objects.filter(category='PD')
    new_arrivals_products = Product.objects.filter(category='NA')
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/dishes.html",locals())




def about(request):
    all_products = Product.objects.all()
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())




def morecategory(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/morecategory.html",locals())

class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        # count is used to stop repeatation 
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())


class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/category.html",locals())


class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/productdetail.html",locals())


# class CustomerLoginView(View):

#     def get(self, request):
#         form = LoginForm()
#         totalitem = 0
#         if request.user.is_authenticated:
#             totalitem = len(Cart.objects.filter(user=request.user))
#         return render(request, 'app/login.html', {'form': form, 'totalitem': totalitem})

#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
            
#             user_obj = User.objects.filter(username = username).first()
#             if user_obj is None:
#                 messages.success(request, 'user not found')
#                 return redirect('/accounts/login/')
            
#             profile_obj = Profile.objects.filter(user = user_obj ).first()

#             if not profile_obj.is_verified:
#                 messages.success(request, 'your profile is not verified')
#                 return redirect('/accounts/login/')
            
#             user = authenticate(username = username , password = password)
#             if user is None:
#                 messages.success(request, 'wrong password')
#                 return redirect('/accounts/login/')
            
#             login(request, user)
#             return redirect('/profile')
            
            
#         return render(request, 'app/login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile

def CustomerLoginView(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.error(request, 'User not found. Please register.')
                return redirect('/registration')

            profile_obj = Profile.objects.filter(user=user_obj).first()

            if not profile_obj.is_verified:
                messages.error(request, 'Your profile is not verified. Please register.')
                return redirect('/registration')

            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, 'Invalid password. Please register.')
                return redirect('/registration')

            login(request, user)
            return redirect('/profile')

        return render(request, 'app/login.html')

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred. Please try again later.')
        return render(request, 'app/error.html')  # Render the error template



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        try:
            if form.is_valid():
                
                user = form.save(commit=False)
                user.save()
                email = form.cleaned_data['email']
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = user , auth_token = auth_token)
                profile_obj.save()
                send_mail_after_registration(email , auth_token)


                return redirect("/token")
            else:
                raise ValidationError("Invalid form data")
        except ValidationError as error:
            return render(request, 'app/customerregistration.html', locals())

def success(request):
    return render(request, "app/success.html") 


def token_send(request):
    return render(request, "app/token_send.html") 


def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Email is already verified')
                return redirect('/')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Email is verified')
            return redirect('/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def error_page(request):
    return render(request, 'app/error.html')

def send_mail_after_registration(email , token):
    subject = 'verify'
    message = f'click on link http://127.0.0.1:8000/verify/{token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]  # Assuming the user model has an email field  
    send_mail(subject, message, from_email, recipient_list)        

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulation! Profile is successfully saved")
        else:
            messages.warning(request, "Invalid data entry")
        return render(request, 'app/profile.html',locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html',locals())


class updateAddress(View):
    def get(self,request,pk):
        # it collect value data from the admin site
        add = Customer.objects.get(pk=pk)
        # instance add insert the data the input field
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulation data is updated")
        else:
            messages.warning(request, "Invalid input data")
        return redirect("address")

      

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart", locals())


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 100
        return render(request, 'app/addtocart.html',locals())


def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    famount = 0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 100
    return render(request, 'app/checkout.html',locals())
    




def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    # Retrieve the latest order placed by the user
    order = OrderPlaced.objects.filter(user=user).latest('ordered_date')

    # Check the order status
    status = order.status
    if status == 'Pending':
        subject = 'Order Confirmation'
        message = f"Dear {user.username}, your order has been sent to food hunger check your site to see the status of the order"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)    

    return redirect("/orders")



def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())


def plus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        # after update we get data
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 100
        # library of data to stoe json value
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        # after update we get data
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 100
        # library of data to stoe json value
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        # after update we get data
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 100
        # library of data to stoe json value
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def search(request):
    query = request.GET['search']
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    # using orm
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html",locals())

def khaltipayment(request):
    payload = {
            'amount': 1000,
            'purchase_order_id': 'Test2',
            'purchase_order_name': 'Test',
            'return_url': 'https://test-pay.khalti.com/{pidx}',
            'website_url': 'http://localhost:8000/',            
        }
    url="https://a.khalti.com/api/v2/epayment/initiate/"
    headers={
    "Authorization": "key 084553ea5c7242b7905fa56ea23df7ed"  
}  
    response=requests.post(url,headers=headers,json=payload)
    response.raise_for_status()
    data=response.json()
    payment_url= data["payment_url"]
    return redirect(payment_url)



@login_required
def Review_rate(request):
    if request.method == 'POST':
        try:
            product = request.POST.get('product')
            comment = request.POST.get('comment')
            rate = request.POST.get('rate')
            user = request.user
            status = 'accepted'
            Review.objects.create(user=user, product=product, comment=comment, rate=rate, status=status)
            return redirect('/reviews')
        except:
            return render(request, 'app/reviews.html', {'error': 'An error occurred'})
    else:
        return render(request, 'app/reviews.html')


@login_required
def reviews(request):
    try:
        review_placed = Review.objects.all().order_by('-created_at')
        return render(request, 'app/reviews.html', locals())
    except:
        return render(request, 'app/reviews.html', {'error': 'An error occurred'})
    
def viewreview(request, pk):
    viewreview = get_object_or_404(Review, pk=pk)
    context = {
        'viewreview': viewreview
    }
    return render(request, "app/viewreview.html", context=context)
