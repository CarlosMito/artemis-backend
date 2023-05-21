from django.urls import path, include
from rest_framework import routers
from .views import (
    UserListApiView, InputListApiView, OutputListApiView, text2image
)

router = routers.DefaultRouter()
router.register("api/output", OutputListApiView)
# router.register("api/text2image", Text2ImageApiView)

urlpatterns = [
    path("", include(router.urls)),
    path("api/user", UserListApiView.as_view()),
    path("api/input", InputListApiView.as_view()),
    path("api/text2image", text2image),
]
