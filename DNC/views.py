from django.shortcuts import render, HttpResponse,redirect
from .models import Samples
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q
from .forms import newsample
from django.contrib import messages
import datetime
import re
# Create your views here.
#samplesdata = Samples.objects

def index(request):
    return render(request, "index.html")

def samples(request):
    amples = Samples.objects.all()

    per_page = request.GET.get('selected', 10)

    print(per_page)
    p = Paginator(amples, per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(10)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj,
               'per_page': per_page,
               }
    
    #page_obj = paginator.get_page(page_number)
    #context = {'page_obj': page_obj}
    #context = {
    #    'samples': Samples.objects.all()
    #}
    #print(context)
    return render(request,'table.html', context)


def search_view(request):
    search_query = request.GET.get('q', '')
    selected_value = request.GET.get('selected', '')

    # Filter your model data based on the search query and selected value
    filtered_data = Samples.objects.filter(
        Q(name__icontains=search_query) |  # Adjust fields as needed
        Q(location__icontains=search_query)
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

def new_sample(request):
    date_time = datetime.datetime.now()
    last_id_obj = Samples.objects.last()

    if last_id_obj:
        last_id = last_id_obj.id  # Replace with the actual field name
        numeric_part = re.search(r'\d+$', last_id).group()  # Extract numeric part
        new_numeric_part = str(int(numeric_part) + 1).zfill(len(numeric_part))
        next_id = f'SG-{new_numeric_part}'
    else:
        next_id = ''
    context = {'date_time': date_time,
               'nextid': next_id}
    return render(request, "newsample.html", context)

def submit_new_sample(request):
    if request.method=="POST":
        print('POST called')
        post = newsample(request.POST)
        if post.is_valid():
            print('Successfully Posted...')
            post.save()
            messages.success(request, "Sample added successfully!")
            return redirect(samples)
        else:
            print("Form errors:", post.errors)
    else:
        print('NO POST')
        post = newsample()

    context = {'post': post}
    
    return render(request, "newsample.html", context)

def edit_sample(request):
    return render(request, "editsample.html")

def edit_selected_rows(request):
    selected_row_ids = request.GET.get('ids').split(',')
    rows_data = Samples.objects.filter(id__in=selected_row_ids)  # Fetch data for selected rows
    context = {'rows_data': rows_data}
    return render(request, 'editsample.html', context)


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