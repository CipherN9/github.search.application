from rest_framework import serializers

from api.enums import SearchType


class SearchParametersSerializer(serializers.Serializer):
    search_type = serializers.ChoiceField(
        choices=SearchType.choices,
        help_text='Search type',
    )

    @staticmethod
    def validate_search_type(value: str) -> SearchType:
        return SearchType(value)


class SearchRequestSerializer(serializers.Serializer):
    search_text = serializers.CharField()


class SearchSerializer(SearchParametersSerializer, SearchRequestSerializer):
    pass


class SearchResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    avatar_url = serializers.CharField()
    location = serializers.CharField(allow_null=True)
