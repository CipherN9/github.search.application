import pytest
from django.core.cache import cache

class FakeCache:
    def __init__(self, backend):
        self._backend = backend
    def clear(self):
        return self._backend.clear()
    def delete_pattern(self, pattern):
        return self._backend.clear()
    def __getattr__(self, name):
        return getattr(self._backend, name)

@pytest.fixture(autouse=True)
def clear_cache(mocker):
    cache.clear()
    fake = FakeCache(cache)
    mocker.patch('api.search_views.cache', fake)
