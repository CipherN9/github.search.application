from django.urls import path

from api.search_views import SearchAPIView, clear_search_endpoint_cache

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("search", SearchAPIView.as_view(), name="search-endpoint"),
    path("clear-cache/", clear_search_endpoint_cache, name="clear-search-cache"),
]
