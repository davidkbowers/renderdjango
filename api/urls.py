from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactView, EventViewSet, RegisterViewSet, SubscriberViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'registrations', RegisterViewSet)
router.register(r'subscribers', SubscriberViewSet)

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('', include(router.urls)),
]
