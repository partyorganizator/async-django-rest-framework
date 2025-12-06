from rest_framework.serializers import SerializerMethodField as DRFSerializerMethodField


class AsyncSerializerMethodField(DRFSerializerMethodField):
    """
    Async-enabled serializer method field for custom representations.
    Supports asynchronous method calls for data transformation.
    """
    async def ato_representation(self, attribute):
        method = getattr(self.parent, self.method_name)
        return await method(attribute)
