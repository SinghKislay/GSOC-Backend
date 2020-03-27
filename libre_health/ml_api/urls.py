from django.urls import path
from .views import ImageUnAutheticatedGradView, ImageUnAutheticatedPredView, ImageUnAutheticatedBBoxPredView, ImageUnAutheticatedBBoxView

urlpatterns = [
    path('xray-grad', ImageUnAutheticatedGradView.as_view()),
    path('xray-pred', ImageUnAutheticatedPredView.as_view()),
    path('xray-bbox', ImageUnAutheticatedBBoxView.as_view()),
    path('xray-bbox-pred', ImageUnAutheticatedBBoxPredView.as_view())
]