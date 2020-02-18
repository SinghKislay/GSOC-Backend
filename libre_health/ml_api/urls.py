from django.urls import path
from .views import ImageUnAutheticatedView

urlpatterns = [
    path('xray', ImageUnAutheticatedView.as_view())
]