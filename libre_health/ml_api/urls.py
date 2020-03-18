from django.urls import path
from .views import ImageUnAutheticatedGradView, ImageUnAutheticatedPredView

urlpatterns = [
    path('xray-grad', ImageUnAutheticatedGradView.as_view()),
    path('xray-pred', ImageUnAutheticatedPredView.as_view())
]