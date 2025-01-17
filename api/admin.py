from django.contrib import admin
from django.utils.html import format_html
from .models import Event, Register, Subscriber

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'eventdatetime', 'address', 'price', 'status_colored')
    list_filter = ('eventdatetime', 'cancelled')
    search_fields = ('title', 'description', 'address')
    date_hierarchy = 'eventdatetime'
    ordering = ('-eventdatetime',)
    
    def status_colored(self, obj):
        color = 'red' if obj.cancelled else 'green'
        status_text = 'Cancelled' if obj.cancelled else 'Active'
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            status_text
        )
    status_colored.short_description = 'Status'

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('email', 'event', 'date_registered', 'status_colored')
    list_filter = ('event', 'date_registered', 'cancelled')
    search_fields = ('email', 'event__title')
    date_hierarchy = 'date_registered'
    ordering = ('-date_registered',)
    
    def status_colored(self, obj):
        color = 'red' if obj.cancelled else 'green'
        status_text = 'Cancelled' if obj.cancelled else 'Active'
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            status_text
        )
    status_colored.short_description = 'Status'

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subscription_status')
    list_filter = ('opted_out',)
    search_fields = ('name', 'email')
    ordering = ('name',)
    
    def subscription_status(self, obj):
        color = 'red' if obj.opted_out else 'green'
        status_text = 'Opted Out' if obj.opted_out else 'Subscribed'
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            status_text
        )
    subscription_status.short_description = 'Status'

# Register models with custom admin classes
admin.site.register(Event, EventAdmin)
admin.site.register(Register, RegisterAdmin)
admin.site.register(Subscriber, SubscriberAdmin)

# Customize admin site header and title
admin.site.site_header = 'Event Management System'
admin.site.site_title = 'EMS Admin Portal'
admin.site.index_title = 'Welcome to EMS Admin Portal'
