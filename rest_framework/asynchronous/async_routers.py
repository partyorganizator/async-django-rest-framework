from rest_framework.routers import (
    DefaultRouter as DRFDefaultRouter,
)
from rest_framework.routers import (
    SimpleRouter as DRFSimpleRouter,
)


class AsyncSimpleRouter(DRFSimpleRouter):
    """
    Async-aware simple router with action mapping support.
    Automatically maps sync actions to async equivalents.
    """
    sync_to_async_action_map = {
        "list": "alist",
        "create": "acreate",
        "retrieve": "aretrieve",
        "update": "aupdate",
        "destroy": "adestroy",
        "partial_update": "partial_aupdate",
    }

    def get_method_map(self, viewset, method_map):
        """
        Given a viewset, and a mapping of http methods to actions,
        return a new mapping which only includes any mappings that
        are actually implemented by the viewset.

        To allow the use of a single router that registers sync and async
        viewsets, the actions defined in the routes' method maps are
        updated to be the "a"-prefixed names for async viewsets.
        """
        bound_methods = {}
        if getattr(viewset, "view_is_async", False):
            method_map = {
                method: self.sync_to_async_action_map.get(action, action)
                for method, action in method_map.items()
            }
        for method, action in method_map.items():
            if hasattr(viewset, action):
                bound_methods[method] = action
        return bound_methods


class AsyncDefaultRouter(AsyncSimpleRouter, DRFDefaultRouter):
    """
    Full-featured async router with API root and format suffix support.
    Extends simple router with additional REST framework features.
    """
    pass
