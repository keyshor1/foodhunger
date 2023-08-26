from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from app.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from inventory.models import *
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.db.models.functions import TruncMinute
from django.db.models import Q



# Create your views here.

def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists  ():
                messages.info(request, 'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFER'))
            
            user_obj = authenticate(username=username , password=password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('/inventory/dashboard/')
            
            else:
                messages.info(request, 'Invalid Password')
                
        
        return render(request , 'inventory/login.html')
    
    except Exception as e:
        print(e)

@login_required
def dashboard(request):
    return render(request, "inventory/dashboard.html", locals()) 


@login_required
def orderplaced(request):
    orderplaced = OrderPlaced.objects.all().order_by('-ordered_date')
    return render(request, "inventory/orderplaced.html", locals())

@login_required
def orderplaced_view(request, pk):
    orderplaced = get_object_or_404(OrderPlaced, pk=pk)
    context = {
        'orderplaced': orderplaced
    }
    return render(request, "inventory/vieworderplaced.html", context=context)

@login_required
def delete_orderplaced(request, pk):
    orderplaced = get_object_or_404(OrderPlaced, pk=pk)
    orderplaced.delete()
    return redirect('/inventory/dashboard/')

@login_required
def update_orderplaced(request, pk):
    orderplaced = get_object_or_404(OrderPlaced, pk=pk)
    if request.method == "POST":
       updateForm = UpdateorderplacedForm(data=request.POST)
       if updateForm.is_valid():
           orderplaced.comment = updateForm.data['quantity']
           orderplaced.rate = updateForm.data['customer']
           orderplaced.status = updateForm.data['status']
           orderplaced.save()
           return redirect(f"/inventory/vieworderplaced/{pk}")
       
    else: 
        updateForm = UpdateorderplacedForm(instance=orderplaced)
    
    context = {"form": updateForm}
    return render(request, "inventory/Editorderplaced.html", context=context)



def searchorderplaced(request):
    query = request.GET.get('searchorderplaced', '')
    if query:
        # Case-insensitive search for the user's username
        searchorderplaced = OrderPlaced.objects.filter(user__username__icontains=query)
    else:
        searchorderplaced = []

    return render(request, "inventory/searchorderplaced.html", {'searchorderplaced': searchorderplaced})



@login_required
def Reviews(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, "inventory/Feedback.html", locals())

@login_required
def review_view(request, pk):
    reviews = get_object_or_404(Review, pk=pk)
    context = {
        'Review': reviews
    }
    return render(request, "inventory/viewFeedback.html", context=context)

@login_required
def delete_review(request, pk):
    Reviews = get_object_or_404(Review, pk=pk)
    Reviews.delete()
    return redirect('/inventory/dashboard/') 

@login_required
def addReviews(request):
    if request.method == "POST":
        try:
            product = request.POST.get('product')
            comment = request.POST.get('comment')
            rate = request.POST.get('rate')
            user = request.user
            status = 'accepted'
            Review.objects.create(user=user, product=product, comment=comment, rate=rate, status=status)

            # Customer_Name = request.POST.get('Customer_Name')
            # Feedback = request.POST.get('Feedback')
            # Review.objects.create(product = Customer_Name, comment = Feedback)
            return redirect('/inventory/dashboard/')
        except:
            return render(request, 'inventory/AddFeedback.html', {'error': 'An error occurred'})
    else:
        return render(request, 'inventory/AddFeedback.html')

@login_required    
def update_review(request, pk):
    reviews = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
       updateForm = UpdateReviewForm(data=request.POST)
       if updateForm.is_valid():
           reviews.product = updateForm.data['product']
           reviews.comment = updateForm.data['comment']
           reviews.rate = updateForm.data['rate']
           reviews.status = updateForm.data['status']
           reviews.save()
           return redirect(f"/inventory/viewReview/{pk}")
       
    else: 
        updateForm = UpdateReviewForm(instance=reviews)
    
    context = {"form": updateForm}
    return render(request, "inventory/Editreview.html", context=context)




# @login_required
# def add_cabin_order(request):
#     cabinorders = Cabin.objects.all()
#     if request.method == "POST":
#         form = AddCabinOrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/inventory/dashboard/')  # Redirect to the appropriate page after saving
#     else:
#         form = AddCabinOrderForm()

#     context = {'form': form}
#     return render(request, 'inventory/AddCabinOrder.html', context)


@login_required
def billing(request):
    if request.method == "POST":
        # Get the list of selected cabin order IDs from the form
        selected_order_ids = request.POST.getlist('selected_orders')
        
        for selected_order_id in selected_order_ids:
            # Get the selected cabin order using its ID
            selected_order = get_object_or_404(Cabinorder, id=selected_order_id)
            user = request.user
            cabin = selected_order.cabin
            
            # Calculate the total price for the selected order
            total_price = selected_order.product.discounted_price * selected_order.quantity

            # Create a billing entry for the selected order
            Billing.objects.create(
                user=user,
                cabin=cabin,
                product=selected_order.product,
                quantity=selected_order.quantity,
                total_price=total_price,
                status='Pending'
            )

            # Delete the selected order as it's being billed
            selected_order.delete()

        # You might want to perform additional actions after creating billing entries

    # Retrieve all cabin orders for display
    cabin_orders = Cabinorder.objects.all()
    billing_instance = Billing.objects.all().order_by('-billing_date')
    # Render the billing template with the list of cabin orders
    return render(request, 'inventory/billing_template.html', locals())

def cabinorder_search(request):
    query = request.GET['search']
    # using orm
    billing_date = Billing.objects.filter(Q(billing_date__icontains=query)).order_by('-billing_date')
    return render(request,"inventory/cabinorder_search.html",locals())



@login_required
def billing_summary(request):
    billing_summary = (
        Billing.objects.annotate(billing_datetime_truncated=TruncMinute('billing_date'))
        .values('billing_datetime_truncated', 'cabin__cabinnumber')
        .annotate(total_price_sum=Sum('total_price'))
        .order_by('-billing_datetime_truncated', 'cabin__cabinnumber')
    )

    grand_total_price = Billing.objects.aggregate(total=Sum('total_price'))['total']

    return render(request, 'inventory/billing_summary.html', {'billing_summary': billing_summary, 'grand_total_price': grand_total_price})


@login_required
def ordercabin(request):
    cabins = Cabin.objects.all()
    cabinorders = Cabinorder.objects.all()
    return render(request, "inventory/ordercabin.html", locals())

@login_required
def view_cabin_orders(request, pk):
    cabin = get_object_or_404(Cabin, pk=pk)
    cabin_orders = Cabinorder.objects.filter(cabin=cabin)

    grand_total = 0  # Initialize the grand total

    for cabin_order in cabin_orders:
        cabin_order.total_price = cabin_order.product.discounted_price * cabin_order.quantity
        grand_total += cabin_order.total_price  # Add each cabin order's total price to the grand total

    return render(request, "inventory/viewcabinorder.html", {'cabin': cabin, 'cabin_orders': cabin_orders, 'grand_total': grand_total})

@login_required
def add_cabin_order_with_cabin(request):
    if request.method == "POST":
        form = AddCabinOrderWithCabinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ordercabin')  # Redirect to the appropriate page after saving
    else:
        form = AddCabinOrderWithCabinForm()

    context = {'form': form}
    return render(request, 'inventory/AddCabinOrder.html', context)

@login_required
def add_cabin_order_without_cabin(request, cabin_pk):
    cabin = get_object_or_404(Cabin, pk=cabin_pk)
    
    if request.method == "POST":
        form = AddCabinOrderWithoutCabinForm(request.POST)
        if form.is_valid():
            cabin_order = form.save(commit=False)
            cabin_order.cabin = cabin
            cabin_order.save()
            return redirect('view_cabin_orders', pk=cabin.pk)  # Redirect to the same page after saving
    else:
        form = AddCabinOrderWithoutCabinForm()

    context = {'form': form, 'cabin': cabin}
    return render(request, 'inventory/AddCabinOrder.html', context)



def delete_cabin_order(request, pk):
    cabin_order = get_object_or_404(Cabinorder, pk=pk)
    cabin_order.delete()
    return redirect('view_cabin_orders', cabin_order.cabin.id)




@login_required
def cabins(request):
    cabins = Cabin.objects.all()
    return render(request, "inventory/cabins.html", locals())



@login_required
def cabin_view(request, pk):
    cabin = get_object_or_404(Cabin, pk=pk)
    context = {'cabin': cabin}
    return render(request, 'inventory/view_cabin.html', context=context)



@login_required
def addcabin(request):
    if request.method == 'POST':
        form = CabinForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/inventory/dashboard/')  # Redirect to the dashboard or desired page
        else:
            return render(request, 'inventory/addcabin.html', {'form': form, 'error': 'An error occurred'})
    else:
        form = CabinForm()
    
    return render(request, 'inventory/addcabin.html', {'form': form})



@login_required
def delete_cabin(request, pk):
    cabin = get_object_or_404(Cabin, pk=pk)
    cabin.delete()
    return redirect('cabin')    

@login_required
def update_cabin(request, pk):
    cabin = get_object_or_404(Cabin, pk=pk)
    if request.method == "POST":
        updateForm = UpdateCabinForm(request.POST, request.FILES, instance=cabin)
        if updateForm.is_valid():
            updateForm.save()
            return redirect(f"/inventory/viewcabin/{pk}")
    else: 
        updateForm = UpdateCabinForm(instance=cabin)

    context = {"form": updateForm}
    return render(request, "inventory/EditCabin.html", context=context)


@login_required
def Products(request):
    products = Product.objects.all()
    return render(request, "inventory/Products.html", locals())

@login_required
def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, "inventory/viewProduct.html", context=context)

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('/inventory/dashboard/')

@login_required
def addProduct(request):
    if request.method == "POST":
        try:
            title = request.POST.get('title')
            selling_price = request.POST.get('selling_price')
            discounted_price = request.POST.get('discounted_price')
            description = request.POST.get('description')
            composition = request.POST.get('composition')
            prodapp = request.POST.get('prodapp')
            category = request.POST.get('category')
            product_image = request.FILES.get('product_image')
            Product.objects.create(
                title=title,
                selling_price=selling_price,
                discounted_price=discounted_price,
                description=description,
                composition=composition,
                prodapp=prodapp,
                category=category,
                product_image=product_image
            )

            return redirect('/inventory/dashboard/')
        except:
            return render(request, 'inventory/AddProduct.html', {'error': 'An error occurred'})
    else:
        return render(request, 'inventory/AddProduct.html')
    
@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        updateForm = UpdateProductForm(request.POST, request.FILES, instance=product)
        if updateForm.is_valid():
            updateForm.save()
            return redirect(f"/inventory/viewProduct/{pk}")
    else: 
        updateForm = UpdateProductForm(instance=product)

    context = {"form": updateForm}
    return render(request, "inventory/EditProduct.html", context=context)

def searchproduct(request):
    query = request.GET.get('searchproduct', '')
    if query:
        searchproduct = Product.objects.filter(title__icontains=query)
    else:
        searchproduct = []
    return render(request, "inventory/searchproduct.html", {'searchproduct': searchproduct})














