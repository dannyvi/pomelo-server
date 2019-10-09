"""
Provide MinorRoute as DefaultRouter in pomelo projects.

As the `patch` method is not allowed in some occasions, we just replaced it
with `post` method.
"""

from rest_framework.routers import DefaultRouter, Route, DynamicRoute


class MinorRouter(DefaultRouter):
    """The DefaultRouter replaced patch method with post."""
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                # 'patch': 'update',  # seems that we don't need this..
                'put': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}),
    ]

    def __init__(self, *args, **kwargs):
        trailing_slash = kwargs.pop('trailing_slash', False)
        super().__init__(trailing_slash=trailing_slash, *args, **kwargs)
