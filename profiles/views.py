from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import ProducerProfile, ProcessorProfile, Product, ProductionEvent, FacilityPhoto, PlantationPhoto, ProducerPhoto, ProcessorPhoto
from .forms import ProducerProfileForm, ProcessorProfileForm, ProductForm, ProductionEventForm
from messaging.models import Message, PartnershipRequest

# Create your views here.

@login_required
def producer_dashboard(request):
    try:
        profile = ProducerProfile.objects.get(user=request.user)
    except ProducerProfile.DoesNotExist:
        profile = ProducerProfile.objects.create(user=request.user)
    
    products = Product.objects.filter(producer=profile)
    events = ProductionEvent.objects.filter(producer=profile)
    
    context = {
        'profile': profile,
        'products': products,
        'events': events,
    }
    return render(request, 'profiles/producer_dashboard.html', context)

@login_required
def add_product(request):
    profile = get_object_or_404(ProducerProfile, user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.producer = profile
            product.save()
            messages.success(request, 'Produit ajouté avec succès.')
            return redirect('producer_dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'profiles/product_form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def edit_product(request, product_id):
    profile = get_object_or_404(ProducerProfile, user=request.user)
    product = get_object_or_404(Product, id=product_id, producer=profile)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit mis à jour avec succès.')
            return redirect('producer_dashboard')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'profiles/product_form.html', {'form': form, 'action': 'Modifier'})

@login_required
def delete_product(request, product_id):
    profile = get_object_or_404(ProducerProfile, user=request.user)
    product = get_object_or_404(Product, id=product_id, producer=profile)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produit supprimé avec succès.')
        return redirect('producer_dashboard')
    
    return render(request, 'profiles/confirm_delete.html', {'object': product})

@login_required
def add_event(request):
    profile = get_object_or_404(ProducerProfile, user=request.user)
    
    if request.method == 'POST':
        form = ProductionEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.producer = profile
            event.save()
            messages.success(request, 'Événement ajouté avec succès.')
            return redirect('producer_dashboard')
    else:
        form = ProductionEventForm()
    
    return render(request, 'profiles/event_form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def edit_event(request, event_id):
    profile = get_object_or_404(ProducerProfile, user=request.user)
    event = get_object_or_404(ProductionEvent, id=event_id, producer=profile)
    
    if request.method == 'POST':
        form = ProductionEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Événement mis à jour avec succès.')
            return redirect('producer_dashboard')
    else:
        form = ProductionEventForm(instance=event)
    
    return render(request, 'profiles/event_form.html', {'form': form, 'action': 'Modifier'})

@login_required
def delete_event(request, event_id):
    profile = get_object_or_404(ProducerProfile, user=request.user)
    event = get_object_or_404(ProductionEvent, id=event_id, producer=profile)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Événement supprimé avec succès.')
        return redirect('producer_dashboard')
    
    return render(request, 'profiles/confirm_delete.html', {'object': event})

@login_required
def profile_detail(request):
    if request.user.user_type == 'producer':
        profile, created = ProducerProfile.objects.get_or_create(user=request.user)
        form = ProducerProfileForm(instance=profile)
        if request.method == 'POST':
            form = ProducerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                # Gérer l'upload de la photo de profil
                if 'profile_photo' in request.FILES:
                    request.user.profile_photo = request.FILES['profile_photo']
                    request.user.save()
                form.save()
                messages.success(request, 'Profil mis à jour avec succès !')
                return redirect('profile_detail')
        return render(request, 'profiles/profile_detail.html', {
            'producer_profile': profile,
            'form': form,
            'user': request.user
        })
    else:
        profile, created = ProcessorProfile.objects.get_or_create(user=request.user)
        form = ProcessorProfileForm(instance=profile)
        if request.method == 'POST':
            form = ProcessorProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                # Gérer l'upload de la photo de profil
                if 'profile_photo' in request.FILES:
                    request.user.profile_photo = request.FILES['profile_photo']
                    request.user.save()
                form.save()
                messages.success(request, 'Profil mis à jour avec succès !')
                return redirect('profile_detail')
        return render(request, 'profiles/profile_detail.html', {
            'processor_profile': profile,
            'form': form,
            'user': request.user
        })

@login_required
def profile_list(request):
    if request.user.user_type == 'producer':
        profiles = ProcessorProfile.objects.all().select_related('user')
    else:
        profiles = ProducerProfile.objects.all().select_related('user')
    
    return render(request, 'profiles/profile_list.html', {
        'profiles': profiles,
        'user': request.user
    })

@login_required
def profile_view(request, pk):
    if request.user.user_type == 'producer':
        profile = get_object_or_404(ProcessorProfile, pk=pk)
    else:
        profile = get_object_or_404(ProducerProfile, pk=pk)
    
    return render(request, 'profiles/profile_view.html', {
        'profile': profile
    })

@login_required
def profile_edit(request):
    if request.user.user_type == 'producer':
        profile = get_object_or_404(ProducerProfile, user=request.user)
        form = ProducerProfileForm(instance=profile)
    else:
        profile = get_object_or_404(ProcessorProfile, user=request.user)
        form = ProcessorProfileForm(instance=profile)

    if request.method == 'POST':
        if request.user.user_type == 'producer':
            form = ProducerProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = ProcessorProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profile_detail')

    return render(request, 'profiles/profile_edit.html', {
        'form': form,
        'profile': profile
    })

@login_required
def processor_dashboard(request):
    try:
        profile = ProcessorProfile.objects.get(user=request.user)
    except ProcessorProfile.DoesNotExist:
        profile = ProcessorProfile.objects.create(user=request.user)
    
    # Statistiques
    partnership_count = PartnershipRequest.objects.filter(
        sender=request.user, 
        status='accepted'
    ).count()
    
    unread_messages = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()
    
    context = {
        'profile': profile,
        'partnership_count': partnership_count,
        'unread_messages': unread_messages,
    }
    return render(request, 'profiles/processor_dashboard.html', context)

@login_required
def upload_facility_photo(request):
    if request.method == 'POST' and request.user.user_type == 'processor':
        processor_profile = get_object_or_404(ProcessorProfile, user=request.user)
        if 'image' in request.FILES:
            FacilityPhoto.objects.create(
                processor=processor_profile,
                image=request.FILES['image'],
                description=request.POST.get('description', '')
            )
            messages.success(request, 'Photo d\'installation ajoutée avec succès !')
    return redirect('profile_detail')

@login_required
def delete_facility_photo(request, photo_id):
    if request.method == 'POST' and request.user.user_type == 'processor':
        photo = get_object_or_404(FacilityPhoto, id=photo_id, processor__user=request.user)
        photo.delete()
        messages.success(request, 'Photo d\'installation supprimée avec succès !')
    return redirect('profile_detail')

@login_required
def upload_plantation_photo(request):
    if request.method == 'POST' and request.user.user_type == 'processor':
        processor_profile = get_object_or_404(ProcessorProfile, user=request.user)
        if 'image' in request.FILES:
            PlantationPhoto.objects.create(
                processor=processor_profile,
                image=request.FILES['image'],
                description=request.POST.get('description', '')
            )
            messages.success(request, 'Photo de plantation ajoutée avec succès !')
    return redirect('profile_detail')

@login_required
def delete_plantation_photo(request, photo_id):
    if request.method == 'POST' and request.user.user_type == 'processor':
        photo = get_object_or_404(PlantationPhoto, id=photo_id, processor__user=request.user)
        photo.delete()
        messages.success(request, 'Photo de plantation supprimée avec succès !')
    return redirect('profile_detail')

@login_required
def upload_producer_photo(request):
    if request.method == 'POST':
        try:
            profile = ProducerProfile.objects.get(user=request.user)
            photo = ProducerPhoto(
                producer=profile,
                image=request.FILES['image'],
                description=request.POST.get('description', ''),
                photo_type=request.POST.get('photo_type', 'plantation')
            )
            photo.save()
            messages.success(request, 'Photo ajoutée avec succès !')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout de la photo : {str(e)}')
    return redirect('profile_detail')

@login_required
def delete_producer_photo(request, photo_id):
    photo = get_object_or_404(ProducerPhoto, id=photo_id, producer__user=request.user)
    photo.delete()
    messages.success(request, 'Photo supprimée avec succès !')
    return redirect('profile_detail')

@login_required
def upload_processor_photo(request):
    if request.method == 'POST':
        try:
            profile = ProcessorProfile.objects.get(user=request.user)
            photo = ProcessorPhoto(
                processor=profile,
                image=request.FILES['image'],
                description=request.POST.get('description', ''),
                photo_type=request.POST.get('photo_type', 'facility')
            )
            photo.save()
            messages.success(request, 'Photo ajoutée avec succès !')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'ajout de la photo : {str(e)}')
    return redirect('profile_detail')

@login_required
def delete_processor_photo(request, photo_id):
    photo = get_object_or_404(ProcessorPhoto, id=photo_id, processor__user=request.user)
    photo.delete()
    messages.success(request, 'Photo supprimée avec succès !')
    return redirect('profile_detail')
