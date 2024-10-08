from django.urls import path

from .views import FeatureView


urlpatterns = [
    path('features/', FeatureView.as_view(), name='feature_view'),
]