from django.shortcuts import render, HttpResponse,redirect, get_object_or_404
from .models import Samples, CuppingSCI, SampleShare, ViewPerms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseNotFound
from django.http import HttpRequest, JsonResponse,HttpResponseForbidden
from django.db.models import Q
from .forms import newsample, RegistrationForm, LoginForm, changesample
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory
import datetime
import re
from django.db import IntegrityError


#A Work in progress...

def get_allowed_fields(user, sample):
    try:
        # Try to get an existing ViewPerms object for the user and sample
        view_perms = ViewPerms.objects.get(user_id=user.id, sample_id=sample.id)
    except ViewPerms.DoesNotExist:
        print('Creating Perms')
        # If it doesn't exist, create a new one
        try:
            view_perms = ViewPerms.objects.create(user=user, sample_id=sample)
            #print(str(view_perms), 'PERMS!!!!!!!NEW')
        except IntegrityError as e:
            # Handle any integrity error if needed
            view_perms = None
            print('integ error:',e)
    if view_perms:
        # Use the view_perms object to determine allowed fields
        allowed_fields = [field.name for field in sample._meta.fields if getattr(view_perms, field.name)]
    else:
        # Handle the case where there was an error creating the ViewPerms object
        allowed_fields = []
    print(allowed_fields, "!!!!!!!!!!!@")
    return allowed_fields

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

    # Fetch samples owned by the user
    user_samples = list(Samples.objects.filter(user=user).order_by('-id'))

    # Fetch shared samples
    shared_samples = list(request.user.shared_samples.all().order_by('-id'))

    # Combine the two lists and remove duplicates
    amples = list(set(user_samples + shared_samples))

    # Define a function to extract the numeric part from the ID
    def extract_numeric_part(sample):
        match = re.match(r'SG-(\d+)', sample.id)
        if match:
            return int(match.group(1))
        return 0  # Return 0 if there's no numeric part

    # Sort the list based on the extracted numeric part in descending order
    amples.sort(key=extract_numeric_part, reverse=True)

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

    return render(request, 'table.html', context)

@login_required
def search_view(request):
    user = request.user
    search_query = request.GET.get('q', '')
    selected_value = request.GET.get('selected', '')

    # Filter your model data based on the search query and selected value
    filtered_data = Samples.objects.filter(
        Q(name__icontains=search_query) |
        Q(location__icontains=search_query) |
        Q(sensorial__icontains=search_query),
        user=user
    ).order_by('-id')

    sharesamplequery = request.user.shared_samples.filter(
        Q(name__icontains=search_query) |
        Q(location__icontains=search_query)|
        Q(sensorial__icontains=search_query)
    ).order_by('-id')

    # Convert querysets to lists
    filtered_data_list = list(filtered_data)
    sharesamplequery_list = list(sharesamplequery)

    # Merge the lists and remove duplicates
    merged_list = filtered_data_list + sharesamplequery_list
    unique_merged_list = list({sample.id: sample for sample in merged_list}.values())

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
        for item in unique_merged_list
    ]

    return JsonResponse(data_list, safe=False)

@login_required
def new_sample(request):
    user = request.user
    date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
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
    date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
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
    
    # Fetch data for selected rows and check if the user has permission to edit each sample
    rows_data = []
    for sample_id in selected_row_ids:
        sample = get_object_or_404(Samples, id=sample_id)
        
        # Check if the sample belongs to the user or is shared with them with can_alter=True
        if sample.user == user or sample.sampleshare_set.filter(user=user, can_alter=1).exists():
            rows_data.append(sample)
        else:
            # If the user doesn't have permission, return a 403 Forbidden response
            return HttpResponseForbidden("You don't have permission to edit this sample.")
    
    context = {
        'rows_data': rows_data,
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
            form = changesample(request.POST, instance=instance)
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
    date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
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
            total_cup_score=request.POST.get(sample_id+'final_cup_score_value'),
            user=user
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
    print('sample_view call user:', user.id)
    date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    try:
        sample = Samples.objects.get(id=coffee_id)
    except Samples.DoesNotExist:
        # Handle the case where the coffee with the given ID doesn't exist
        return HttpResponseNotFound("Sample not found")

    # Check if the user is the same as the sample's user
    if user.id == sample.user.id:
        allowed_fields = [field.name for field in sample._meta.fields]
        print(allowed_fields, "owner")
    else:
        allowed_fields = get_allowed_fields(user, sample)
        print(allowed_fields, "not owner!@")

    # Create a dictionary to store field values
    field_values = {}
    for field_name in allowed_fields:
        field_value = getattr(sample, field_name)
        field_values[field_name] = field_value
        # Set values for fields not in allowed_fields to "No Permissions"

    for field_name in sample._meta.fields:
        print(field_name.name, "name! exist!")
        if field_name.name not in allowed_fields:
            print(field_name.name, "name!")
            field_values[field_name.name] = "No Permissions"
    print(field_values, "!!!!!!")

    try:
        cupsession = CuppingSCI.objects.filter(sample_id=coffee_id, user=user.id)
    except CuppingSCI.DoesNotExist:
        cupsession = "No cupping data found!"
        print(cupsession)
        context = {
            'global_session': cupsessions,
            'cup_session': cupsession,
            'sample_id': coffee_id,
            'user_first_name': user.first_name,
            'user_last_name': user.last_name,
            'sample': sample,
            'user_id': user.id,
            'field_values': field_values,
            'allowed_fields': allowed_fields,  # Pass the allowed fields to the template
        }
        return render(request, 'sampleview.html', context)

    try:
        cupsessions = CuppingSCI.objects.filter(sample_id=coffee_id)
    except CuppingSCI.DoesNotExist:
        cupsessions = "No cupping data found!"
        print(cupsessions)
        context = {
            'global_session': cupsessions,
            'cup_session': cupsession,
            'sample_id': coffee_id,
            'user_first_name': user.first_name,
            'user_last_name': user.last_name,
            'sample': sample,
            'user_id': user.id,
            'field_values': field_values,
            'allowed_fields': allowed_fields,  # Pass the allowed fields to the template
        }
        return render(request, 'sampleview.html', context)

    context = {
            'global_session': cupsessions,
            'cup_session': cupsession,
            'sample_id': coffee_id,
            'user_first_name': user.first_name,
            'user_last_name': user.last_name,
            'sample': sample,
            'user_id': user.id,
            'field_values': field_values,
            'allowed_fields': allowed_fields,  # Pass the allowed fields to the template
        }
    print(cupsession)
    return render(request, 'sampleview.html', context)


@login_required
def search_users(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        search_query = request.GET.get('search_query', '')
        # Query the users based on the search query
        users = User.objects.filter(username__icontains=search_query)[:10]  # Adjust the query as needed
        user_list = [{'username': user.username, 'email': user.email, 'id': user.id} for user in users]
        return JsonResponse({'users': user_list})
    else:
        # If it's not an AJAX request, return an empty JSON response or handle it as needed
        return JsonResponse({})


@login_required
def add_to_shared(request):
    if request.method == 'POST':
        username_id = request.POST.get('username_id')
        sample_ids = request.POST.get('sample_ids')
        allow_alter = request.POST.get('allow_alter')  # Get the 'allow_alter' value
        
        try:
            # Get the User instance based on the username_id
            user_to_share_with = get_object_or_404(User, id=username_id)
            
            # Split the sample_ids into a list
            sample_ids_list = sample_ids.split(',')
            
            # Iterate through the sample IDs
            for sample_id in sample_ids_list:
                # Get the Samples instance based on sample_id
                sample = get_object_or_404(Samples, id=sample_id)
                
                # Check if the requesting user is the original creator of the sample
                if sample.user != request.user:
                    return JsonResponse({'success': False, 'error': 'You cannot share samples that you do not own!'})
                
                # Check if a share already exists for this user and sample
                share, created = SampleShare.objects.get_or_create(
                    user=user_to_share_with,
                    sample=sample
                )
                
                # Update the 'can_alter' field based on 'allow_alter'
                share.can_alter = allow_alter == 'true'
                share.save()
                print('alter: ', allow_alter)

                if share.can_alter:
                    try:
        # Check if ViewPerms already exist for this user and sample
                        existing_perms = ViewPerms.objects.filter(user=user_to_share_with, sample=sample).first()
        
                        if existing_perms:
            # Update the existing ViewPerms object
                            for field in existing_perms._meta.fields:
                                if field.name not in ['sample_id', 'user_id', 'sample', 'user', 'id']:
                                    setattr(existing_perms, field.name, True)
                            existing_perms.save()
                            print("Existing permissions updated")
                        else:
            # Create a new ViewPerms object
                            new_perms = ViewPerms.objects.create(user=user_to_share_with, sample=sample)

            # Set sample_id and user_id manually
                            new_perms.sample_id = sample.id
                            new_perms.user_id = user_to_share_with.id

            # Iterate over the other fields and set them to True
                            for field in new_perms._meta.fields:
                                if field.name not in ['sample_id', 'user_id', 'sample', 'user', 'id']:
                                    setattr(new_perms, field.name, True)

                            new_perms.save()
                            print('New permissions created')
                    except Exception as e:
                        print('Did not create or update viewing permissions:', e)
                else:
                    print('Cannot alter, permissions will be set automatically later')

            return JsonResponse({'success': True})
        
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False})

@login_required
def delete_selected_samples(request):
    sample_ids = request.POST.get('sample_ids', '').split(',')
    user = request.user
    
    # Iterate through the selected sample IDs
    for sample_id in sample_ids:
        sample = get_object_or_404(Samples, id=sample_id)
        
        # Check if the user is the owner of the sample
        if sample.user == user:
            # Delete the sample since the user is the owner
            sample.delete()
        else:
            # Check if it's a shared sample
            sample_share = SampleShare.objects.filter(sample=sample, user_id=user).first()
            if sample_share:
                # Remove the SampleShare instance
                sample_share.delete()
    
    return JsonResponse({'success': True})
