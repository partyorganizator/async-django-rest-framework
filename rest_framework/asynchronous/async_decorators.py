import asyncio
import types


from asynchronous.async_views import AsyncAPIView


def aapi_view(http_method_names=None):
    """
    Async decorator converting functions to APIView subclasses.
    Supports both sync and async function-based views seamlessly.
    """
    http_method_names = ["GET"] if (http_method_names is None) else http_method_names

    def decorator(func):
        WrappedAPIView = type("WrappedAPIView", (AsyncAPIView,), {"__doc__": func.__doc__})

        # Note, the above allows us to set the docstring.
        # It is the equivalent of:
        #
        #     class WrappedAPIView(APIView):
        #         pass
        #     WrappedAPIView.__doc__ = func.doc    <--- Not possible to do this

        # api_view applied without (method_names)
        assert not (
            isinstance(http_method_names, types.FunctionType)
        ), "@api_view missing list of allowed HTTP methods"

        # api_view applied with eg. string instead of list of strings
        assert isinstance(http_method_names, (list, tuple)), (
            "@api_view expected a list of strings, received %s"
            % type(http_method_names).__name__
        )

        allowed_methods = set(http_method_names) | {"options"}
        WrappedAPIView.http_method_names = [
            method.lower() for method in allowed_methods
        ]

        view_is_async = asyncio.iscoroutinefunction(func)

        if view_is_async:

            async def handler(self, *args, **kwargs):
                return await func(*args, **kwargs)

        else:

            def handler(self, *args, **kwargs):
                return func(*args, **kwargs)

        for method in http_method_names:
            setattr(WrappedAPIView, method.lower(), handler)

        WrappedAPIView.__name__ = func.__name__
        WrappedAPIView.__module__ = func.__module__

        WrappedAPIView.renderer_classes = getattr(
            func, "renderer_classes", AsyncAPIView.renderer_classes
        )

        WrappedAPIView.parser_classes = getattr(
            func, "parser_classes", AsyncAPIView.parser_classes
        )

        WrappedAPIView.authentication_classes = getattr(
            func, "authentication_classes", AsyncAPIView.authentication_classes
        )

        WrappedAPIView.throttle_classes = getattr(
            func, "throttle_classes", AsyncAPIView.throttle_classes
        )

        WrappedAPIView.permission_classes = getattr(
            func, "permission_classes", AsyncAPIView.permission_classes
        )

        WrappedAPIView.content_negotiation_class = getattr(
            func, "content_negotiation_class", AsyncAPIView.content_negotiation_class
        )

        WrappedAPIView.metadata_class = getattr(
            func, "metadata_class", AsyncAPIView.metadata_class
        )

        WrappedAPIView.versioning_class = getattr(
            func, "versioning_class", AsyncAPIView.versioning_class
        )

        WrappedAPIView.schema = getattr(func, "schema", AsyncAPIView.schema)

        return WrappedAPIView.as_view()

    return decorator
