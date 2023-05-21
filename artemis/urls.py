from django.urls import path, include
from rest_framework import routers
from .views import (
    UserListApiView, InputListApiView, OutputListApiView
)

router = routers.DefaultRouter()
router.register("api/output", OutputListApiView)

urlpatterns = [
    path("", include(router.urls)),
    path("api/user", UserListApiView.as_view()),
    path("api/input", InputListApiView.as_view()),
    # path("api/output", OutputListApiView.as_view(actions={'get': 'list', "post"})),
]
