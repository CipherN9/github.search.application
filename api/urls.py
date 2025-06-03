from django.urls import include, path
from rest_framework import routers

from api import search_views
from api.search_views import SearchAPIView, clear_search_endpoint_cache

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('search', SearchAPIView.as_view()),
    path("clear-cache/", clear_search_endpoint_cache, name="clear-search-cache"),
]