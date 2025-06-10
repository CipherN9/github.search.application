from api.services.service import ServiceLayer
from api.utils.constants import TEST_SEARCH_USERS_RESPONSE
from api.utils.enums import SearchType


def test_service_layer(mocker):
    service_layer = ServiceLayer(search_type=SearchType.USERS)
    mocker.patch.object(service_layer._repository, attribute='get', return_value=TEST_SEARCH_USERS_RESPONSE)
    result = service_layer.search_by_text("string")
    assert result == TEST_SEARCH_USERS_RESPONSE

