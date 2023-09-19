from django.shortcuts import render, HttpResponse,redirect
from .models import Samples, CuppingSCI
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseNotFound
from django.db.models import Q
from .forms import newsample, RegistrationForm, LoginForm, CuppingFormSCI
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
import datetime
import re

#A Work in progress...

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
    amples = Samples.objects.filter(user=user).order_by('-id')
    shared_samples = request.user.shared_samples.all()
    
    amples = amples | shared_samples
    
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
    ).order_by('-id')

    sharesamplequery=request.user.shared_samples.filter(
        Q(name__icontains=search_query) |  # Adjust fields as needed
        Q(location__icontains=search_query)
    ).order_by('-id')
    filtered_data = filtered_data | sharesamplequery
    data_list = [
        {
            'ref': "/sample_view/" + str(item.id),
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
                    username=form.cleaned_data['username'],
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
            user = authenticate(request, email=email, password=password)  # Use email as the username
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

@login_required
def cupping_sci(request):
        # Retrieve the selected_ids query parameter from the URL
    selected_ids = request.GET.get('selected_ids')
    print(selected_ids)
    if selected_ids:
        # Split the selected_ids string into a list
        selected_ids_list = selected_ids.split(',')

        # Now, you have a list of selected IDs (some may be integers, some strings)
        # You can use this list to filter your Django model based on your criteria
        selected_samples = Samples.objects.filter(id__in=selected_ids_list)
        print(selected_samples)
        # Do something with the selected_samples, such as rendering a template
        return render(request, 'cuppingSCI.html', {'selected_samples': selected_samples})
    else:
        # Handle the case where no selected_ids parameter is provided
        return HttpResponse("No selected_ids parameter found in the URL.")
    
@login_required    
def save_session(request):
    user = request.user
    date_time = datetime.datetime.now()
    if request.method == 'POST':
        # Get the list of sample IDs from the form data
        selected_ids = request.POST.getlist('sample_id')

        # Initialize a list to store the created CuppingSCI objects
        created_cupping_sci_list = []
        for sample_id in selected_ids:
            print(sample_id)
            cupping_sci = CuppingSCI(
            sample_id=sample_id,
            roast_level_range=request.POST.get(sample_id+'roast_level_range'),
            ferment_level_range=request.POST.get(sample_id+'ferment_level_range'),
            fragrance_range=request.POST.get(sample_id+'fragrance_range'),
            fragrance_intensity_range=request.POST.get(sample_id+'fragrance_intensity_range'),
            fragrance_notes=request.POST.get(sample_id+'fragrance_notes'),
            flavor_range=request.POST.get(sample_id+'flavor_range'),
            flavor_intensity_range=request.POST.get(sample_id+'flavor_intensity_range'),
            Flavor_notes=request.POST.get(sample_id+'Flavor_notes'),
            aroma_range=request.POST.get(sample_id+'aroma_range'),
            aroma_intensity_range=request.POST.get(sample_id+'aroma_intensity_range'),
            aroma_notes=request.POST.get(sample_id+'aroma_notes'),
            acidity_range=request.POST.get(sample_id+'acid_range'),
            acidity_intensity_range=request.POST.get(sample_id+'acid_Intensity_range'),
            Acidity_notes=request.POST.get(sample_id+'Acidity_notes'),
            body_range=request.POST.get(sample_id+'body_range'),
            body_thickness_range=request.POST.get(sample_id+'body_thickness_range'),
            body_notes=request.POST.get(sample_id+'body_notes'),
            sweetness_range=request.POST.get(sample_id+'sweetness_range'),
            sweetness_intensity_range=request.POST.get(sample_id+'sweetness_intensity_range'),
            sweetness_notes=request.POST.get(sample_id+'sweetness_notes'),
            aftertaste_range=request.POST.get(sample_id+'aftertaste_range'),
            aftertaste_duration_range=request.POST.get(sample_id+'aftertaste_duration_range'),
            aftertaste_notes=request.POST.get(sample_id+'aftertaste_notes'),
            fresh_range=request.POST.get(sample_id+'fresh_range'),
            fresh_woody_range=request.POST.get(sample_id+'fresh_woody_range'),
            freshcrop_notes=request.POST.get(sample_id+'freshcrop_notes'),
            off_1_range=request.POST.get(sample_id+'off_1_range'),
            off_2_range=request.POST.get(sample_id+'off_2_range'),
            off_3_range=request.POST.get(sample_id+'off_3_range'),
            off_4_range=request.POST.get(sample_id+'off_4_range'),
            off_5_range=request.POST.get(sample_id+'off_5_range'),
            off_notes=request.POST.get(sample_id+'off_notes'),
            uniform_1_range=request.POST.get(sample_id+'uniform_1_range'),
            uniform_2_range=request.POST.get(sample_id+'uniform_2_range'),
            uniform_3_range=request.POST.get(sample_id+'uniform_3_range'),
            uniform_4_range=request.POST.get(sample_id+'uniform_4_range'),
            uniform_5_range=request.POST.get(sample_id+'uniform_5_range'),
            uniformity_notes=request.POST.get(sample_id+'uniformity_notes'),
            sens_descriptors=request.POST.get(sample_id+'sens_descriptors'),
            cupdate=date_time,
            total_cup_score=request.POST.get(sample_id+'final_cup_score_value')
            )
            try:
                sample = Samples.objects.get(id=sample_id)
                total_score = request.POST.get(sample_id+'final_cup_score_value')
                print(total_score)
            except Samples.DoesNotExist:
            # Handle the case where the object doesn't exist
            # You can return an error response or redirect as needed
                return redirect('samples')  # Redirect to a sample list view, adjust the URL name as needed

        # Update the 'sensorial' field with the 'total_score'
            sample.sensorial = total_score
            sample.save()

            created_cupping_sci_list.append(cupping_sci)

        # Save the CuppingSCI object to the database
    
        CuppingSCI.objects.bulk_create(created_cupping_sci_list)
        # Redirect to a success page or the next step in your workflow
        return redirect(samples)  # Replace 'success_page' with the actual URL name

    # Handle GET request or any other case
    return render(request, 'index.html')  # Replace 'error_page' with the actual error page template

@login_required
def sample_view(request, coffee_id):
    user = request.user
    date_time = datetime.datetime.now()

    try:
        sample = Samples.objects.get(id=coffee_id)
    except Samples.DoesNotExist:
        # Handle the case where the coffee with the given ID doesn't exist
        return HttpResponseNotFound("Sample not found")
    try:
        cupsession = CuppingSCI.objects.filter(sample_id=coffee_id, user=user.id)
    except CuppingSCI.DoesNotExist:
        cupsession = "No cupping data found!"
        print(cupsession)
        context = {
        'cup_session': cupsession,
        'sample_id': coffee_id,
        'user_first_name': user.first_name,
        'user_last_name': user.last_name,
        'sample': sample,  # Add the sample object to the context
        'user_id': user.id,
        }
        return render(request, 'sampleview.html', context)
    try:
        cupsessions = CuppingSCI.objects.filter(sample_id=coffee_id)
    except CuppingSCI.DoesNotExist:
        cupsessions = "No cupping data found!"
        print(cupsessions)
        context = {
        'global_sessions': cupsessions,
        'cup_session': cupsession,
        'sample_id': coffee_id,
        'user_first_name': user.first_name,
        'user_last_name': user.last_name,
        'sample': sample,  # Add the sample object to the context
        'user_id': user.id,
        }
        return render(request, 'sampleview.html', context)
    context = {
        'global_session': cupsessions,
        'cup_session': cupsession,
        'sample_id': coffee_id,
        'user_first_name': user.first_name,
        'user_last_name': user.last_name,
        'sample': sample,  # Add the sample object to the context
        'user_id': user.id,
    }
    print(cupsession)
    return render(request, 'sampleview.html', context)