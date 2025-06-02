from functools import wraps
from typing import Dict, Optional


class SerializedMixin:
    wrapped_methods = ["get", "post", "put", "patch", "delete"]

    @staticmethod
    def get_query_params(request, method) -> Optional[Dict[str, str]]:
        query_params_serializer_class = getattr(method, "_query_ser", None)
        query_params = None
        if query_params_serializer_class:
            qp_ser = query_params_serializer_class[0](data=request.query_params.dict())
            qp_ser.is_valid(raise_exception=True)
            query_params = qp_ser.validated_data

        return query_params

    @staticmethod
    def get_request_body(request, method) -> Optional[Dict[str, str]]:
        request_body_serializer_class = getattr(method, "_body_ser", None)
        request_body = None
        if request_body_serializer_class:
            if isinstance(request.data, list):
                child = request_body_serializer_class.child
                request_body_serializer_class = request_body_serializer_class.__class__
                request_body_serializer_class.child = child

            rb_ser = request_body_serializer_class(data=request.data)
            rb_ser.is_valid(raise_exception=True)
            request_body = rb_ser.validated_data

        return request_body

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for method in cls.wrapped_methods:
            original_endpoint_method = getattr(cls, method, None)
            if original_endpoint_method is None:
                return

            @wraps(original_endpoint_method)
            def wrapped_endpoint(self, request, *args, **kwargs):
                query_params = self.get_query_params(request, original_endpoint_method)
                request_body = self.get_request_body(request, original_endpoint_method)

                result = original_endpoint_method(self, request, query_params, request_body, *args, **kwargs)

                return result

            setattr(cls, method, wrapped_endpoint)
