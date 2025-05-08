from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Message, PartnershipRequest, Partnership
from .forms import MessageForm, PartnershipRequestForm

User = get_user_model()

@login_required
def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'messaging/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages
    })

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.receiver == request.user:
        message.is_read = True
        message.save()
    return render(request, 'messaging/message_detail.html', {'message': message})

@login_required
def send_message(request, receiver_id=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message envoyé avec succès !')
            return redirect('inbox')
    else:
        initial = {}
        if receiver_id:
            receiver = get_object_or_404(User, pk=receiver_id)
            initial['receiver'] = receiver
        form = MessageForm(initial=initial)
    
    # Récupérer tous les utilisateurs sauf l'utilisateur actuel
    users = User.objects.exclude(id=request.user.id)
    
    return render(request, 'messaging/send_message.html', {
        'form': form,
        'users': users
    })

@login_required
def partnership_requests(request):
    received_requests = PartnershipRequest.objects.filter(receiver=request.user).order_by('-created_at')
    sent_requests = PartnershipRequest.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'messaging/partnership_requests.html', {
        'received_requests': received_requests,
        'sent_requests': sent_requests
    })

@login_required
def send_partnership_request(request, receiver_id):
    receiver = get_object_or_404(User, pk=receiver_id)
    
    if request.method == 'POST':
        form = PartnershipRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.sender = request.user
            request_obj.receiver = receiver
            request_obj.save()
            messages.success(request, 'Demande de partenariat envoyée avec succès !')
            return redirect('partnership_requests')
    else:
        form = PartnershipRequestForm()
    
    return render(request, 'messaging/send_partnership_request.html', {
        'form': form,
        'receiver': receiver
    })

@login_required
def respond_to_partnership_request(request, pk, status):
    partnership_request = get_object_or_404(PartnershipRequest, pk=pk, receiver=request.user)
    
    if status == 'accepted':
        # Vérifier si un partenariat existe déjà
        if not Partnership.objects.filter(
            producer=partnership_request.sender,
            processor=request.user
        ).exists():
            # Créer un nouveau partenariat
            Partnership.objects.create(
                producer=partnership_request.sender,
                processor=request.user,
                request=partnership_request,
                description=partnership_request.message
            )
            messages.success(request, 'Partenariat créé avec succès !')
        else:
            messages.warning(request, 'Un partenariat existe déjà avec cet utilisateur.')
    
    partnership_request.status = status
    partnership_request.save()
    
    return redirect('partnership_requests')

@login_required
def partnership_detail(request, pk):
    partnership = get_object_or_404(Partnership, pk=pk)
    # Vérifier que l'utilisateur est bien partie prenante du partenariat
    if request.user not in [partnership.producer, partnership.processor]:
        messages.error(request, "Vous n'avez pas accès à ce partenariat.")
        return redirect('partnership_requests')
    
    return render(request, 'messaging/partnership_detail.html', {
        'partnership': partnership
    })
