from django.urls import path, include
from rest_framework import routers
from .views import (
    ProfileListApiView, InputListApiView, OutputListApiView, text2image
)

router = routers.DefaultRouter()
router.register("output", OutputListApiView)
# router.register("text2image", Text2ImageApiView)

urlpatterns = [
    path("", include(router.urls)),
    path("profile", ProfileListApiView.as_view()),
    path("input", InputListApiView.as_view()),
    path("text2image", text2image),
]
