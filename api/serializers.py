from rest_framework import serializers
from .models import Event, Register, Subscriber

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Register
        fields = ['id', 'date_registered', 'cancelled', 'email', 'event', 
                 'event_title', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class EventSerializer(serializers.ModelSerializer):
    registrations_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'eventdatetime', 'address', 
                 'price', 'cancelled', 'created_at', 'updated_at', 'registrations_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_registrations_count(self, obj):
        return obj.registrations.filter(cancelled=False).count()

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'name', 'email', 'opted_out', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate_email(self, value):
        """
        Check if email already exists and not opted out
        """
        if self.instance is None:  # Only for creation
            if Subscriber.objects.filter(email=value, opted_out=False).exists():
                raise serializers.ValidationError("This email is already subscribed.")
        return value
