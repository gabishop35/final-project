from django.shortcuts import render, redirect, get_object_or_404
from .models import Lake, Fish, Regulation, Tag, Catch, User, Question
from fishbytes.forms import CatchForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template




# Create your views here.
def homepage(request):
    lakes = Lake.objects.all()
    return render(request, 'base.html', {'lakes': lakes, })

def lake_detail(request, pk):
    lake = Lake.objects.get(pk=pk)
    fishes = Fish.objects.filter(lakes__name__contains=lake.name)
    return render(request, 'core/lake_detail.html', {'lake': lake, 'fishes': fishes, })

def fish_detail(request, pk):
    fish = get_object_or_404(Fish, pk=pk)
    lakes = fish.lakes.all()
    return render(request, "core/fish_detail.html", {'lakes': lakes, 'fish': fish, 'pk': pk})

@login_required
def profile_page(request):
    catches = Catch.objects.filter(user=request.user)
    return render(request, 'core/profile_page.html', {'catches': catches})

@login_required
def add_catch(request):
    if request.method =='POST':
        form = CatchForm(request.POST, request.FILES)
        if form.is_valid():
            catch = form.save(commit=False)
            catch.user = request.user
            catch.save()
            return redirect('profile-page')
    else:
        form = CatchForm()
    return render(request, 'core/add_catch.html', {'form': form})

@login_required
def edit_catch(request, pk):
    catch = get_object_or_404(Catch, pk=pk)
    if request.method == 'POST':
        form = CatchForm(request.POST, request.FILES, instance=catch)
        if form.is_valid():
            catch = form.save(commit=False)
            catch.user = request.user
            catch.save()
            return redirect('profile-page')
    else: 
        form = CatchForm(instance=catch)
    return render(request, 'core/edit_catch.html', {'form': form}) 

def fishid(request):
    questions = Question.objects.all().order_by('pos')
    return render(request, 'core/identify.html', {'questions': questions})

@login_required
def delete_catch(request, pk):
    catch = get_object_or_404(Catch, pk=pk)
    catch.delete()
    return redirect('profile-page')

@login_required
def show_map(request, pk):
    lake = get_object_or_404(Lake, pk=pk)
    lake_center = [lake.location[1], lake.location[0]]
    map = 'pk.mapbox_access_token'
    catches = Catch.objects.filter(user=request.user, lake=lake)
    map_features = [{'type': 'Feature',
                            'properties': {},
                            'geometry': {
                            'type': "Point",
                            'coordinates': [str(catch.longitude), str(catch.latitude)],
                                    }
                                } for catch in catches]
    context={ 
        'map': map, 
        'catches': catches, 
        'mapFeatures': map_features, 
        'lake': lake, 
        'lake_center': lake_center }
    return render(request, 'core/maps.html', context)

def serviceworker(request):
    template = get_template('core/serviceworker.js')
    html = template.render()
    return HttpResponse(html, content_type="application/x-javascript")