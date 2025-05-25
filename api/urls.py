from django.urls import include, path
from rest_framework import routers

from api import views
from api.views import SearchAPIView

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('search', SearchAPIView.as_view()),
]