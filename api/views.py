from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactSerializer, EventSerializer, RegisterSerializer, SubscriberSerializer
from .models import Event, Register, Subscriber

# Create your views here.

class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # Get the validated data
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']
            
            # Prepare email content
            email_subject = f'Contact Form Message from {name}'
            email_message = f'From: {name}\nEmail: {email}\n\nMessage:\n{message}'
            
            try:
                # Send email
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                return Response(
                    {'message': 'Your message has been sent successfully!'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'error': 'Failed to send email. Please try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    def get_queryset(self):
        queryset = Register.objects.all()
        event_id = self.request.query_params.get('event', None)
        if event_id is not None:
            queryset = queryset.filter(event_id=event_id)
        return queryset

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def get_queryset(self):
        # Only show non-opted-out subscribers by default
        return Subscriber.objects.filter(opted_out=False)

    def perform_destroy(self, instance):
        # Instead of deleting, mark as opted out
        instance.opted_out = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
