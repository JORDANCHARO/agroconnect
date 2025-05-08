from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from profiles.models import ProducerProfile, ProcessorProfile
from profiles.forms import ProducerProfileForm, ProcessorProfileForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Créer le profil approprié selon le type d'utilisateur
            if user.user_type == 'producer':
                ProducerProfile.objects.create(user=user)
            else:
                ProcessorProfile.objects.create(user=user)
            
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.user.user_type == 'producer':
        profile, created = ProducerProfile.objects.get_or_create(user=request.user)
        profile_form = ProducerProfileForm(instance=profile)
    else:
        profile, created = ProcessorProfile.objects.get_or_create(user=request.user)
        profile_form = ProcessorProfileForm(instance=profile)

    user_form = CustomUserChangeForm(instance=request.user)

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if request.user.user_type == 'producer':
            profile_form = ProducerProfileForm(request.POST, request.FILES, instance=profile)
        else:
            profile_form = ProcessorProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    
    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'producer_profile': profile if request.user.user_type == 'producer' else None,
        'processor_profile': profile if request.user.user_type == 'processor' else None,
        'user': request.user
    })

@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def user_detail(request, pk):
    user = CustomUser.objects.get(pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})
