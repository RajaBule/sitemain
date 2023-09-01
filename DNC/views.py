from django.shortcuts import render, HttpResponse,redirect
from .models import Samples
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q
from .forms import newsample, RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
import re
# Create your views here.
#samplesdata = Samples.objects

@login_required
def index(request):
    user = request.user
    context = {
        'user_first_name': user.first_name,
        'user_last_name': user.last_name,
    }
    return render(request, 'index.html', context)

@login_required
def samples(request):
    user = request.user
    amples = Samples.objects.filter(user=user)
    
    per_page = request.GET.get('selected', 25)

    print(per_page)
    p = Paginator(amples, per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(25)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj,
               'per_page': per_page,
               'user_first_name': user.first_name,
               'user_last_name': user.last_name,
               }
    
    #page_obj = paginator.get_page(page_number)
    #context = {'page_obj': page_obj}
    #context = {
    #    'samples': Samples.objects.all()
    #}
    #print(context)
    return render(request,'table.html', context)

@login_required
def search_view(request):
    user = request.user
    search_query = request.GET.get('q', '')
    selected_value = request.GET.get('selected', '')

    # Filter your model data based on the search query and selected value
    filtered_data = Samples.objects.filter(
        
        Q(name__icontains=search_query) |  # Adjust fields as needed
        Q(location__icontains=search_query),
        user=user
    )

   
    data_list = [
        {
            'id': item.id,
            'name': item.name,
            'location': item.location,
            'sensorial': item.sensorial,
            'sensorialdescriptors': item.sensorialdescriptors,
            'regdate': item.regdate
        }
        for item in filtered_data
    ]
    
    return JsonResponse(data_list, safe=False)

@login_required
def new_sample(request):
    user = request.user
    date_time = datetime.datetime.now()
    last_id_obj = Samples.objects.last()
    print(date_time)
    if last_id_obj:
        last_id = last_id_obj.id  # Replace with the actual field name
        numeric_part = re.search(r'\d+$', last_id).group()  # Extract numeric part
        new_numeric_part = str(int(numeric_part) + 1).zfill(len(numeric_part))
        next_id = f'SG-{new_numeric_part}'
    else:
        next_id = ''
    context = {'date_time': date_time,
               'nextid': next_id,
               'user_first_name': user.first_name,
               'user_last_name': user.last_name
               }
    
    return render(request, "newsample.html", context)

@login_required
def submit_new_sample(request):
    date_time = datetime.datetime.now()
    user = request.user
    if request.method == "POST":
        print('POST called')
        post = newsample(request.POST)
        if post.is_valid():
            print('Successfully Posted...')
            sample = post.save(commit=False)  # Create an instance but don't save it yet
            sample.user = request.user  # Set the user to the currently logged-in user
            sample.save()  # Now save the instance with the user information
            messages.success(request, "Sample added successfully!")
            return redirect(samples)
        else:
            print("Form errors:", post.errors)
    else:
        print('NO POST')
        post = newsample()

    context = {'post': post,
               'user_first_name': user.first_name,
               'user_last_name': user.last_name,
               'date_time' : date_time,
               }
    
    return render(request, "newsample.html", context)

@login_required
def edit_sample(request):
    user = request.user
    context = {
        'user_first_name': user.first_name,
        'user_last_name': user.last_name
    }
    return render(request, "editsample.html", context)

@login_required
def edit_selected_rows(request):
    user = request.user
    selected_row_ids = request.GET.get('ids').split(',')
    rows_data = Samples.objects.filter(id__in=selected_row_ids)  # Fetch data for selected rows
    context = {'rows_data': rows_data,
               'user_first_name': user.first_name,
               'user_last_name': user.last_name
               }
    return render(request, 'editsample.html', context)

@login_required
def update_selected_row(request):
    if request.method == "POST":
        print('POST CALL-----')
        selected_row_ids = request.POST.getlist('id')  # Get the selected row IDs from the form

        for row_id in selected_row_ids:
            instance = Samples.objects.get(id=row_id)  # Get the existing instance from the database
            form = newsample(request.POST, instance=instance)
            print("MAdE IT THIS FAR--")  # Populate the form with existing instance data
            if form.is_valid():
                form.save() 
                print('SAVEFORM---') # Save the updated data

        messages.success(request, "Samples updated successfully!")
        return redirect('samples')  # Redirect to the samples page or another appropriate URL

    return redirect('edit_selected_rows')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Check if passwords match
            password = form.cleaned_data['password']
            password_repeat = form.cleaned_data['password_repeat']
            if password != password_repeat:
                form.add_error('password_repeat', "Passwords do not match.")
            else:
                # Create user account
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    password=password
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()

                # Log the user in
                user = authenticate(username=user.username, password=password)
                if user:
                    login(request, user)
                    return redirect(index)  # Redirect to your dashboard page
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('index')  # Redirect to your dashboard page
            else:
                form.add_error('email', "Invalid credentials.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to your login page

def cupping_session_sci(request):
    return render(request ,'cuppingSCI.html')