from django.urls import path, include
from rest_framework import routers
from .views import (
    ProfileListApiView, InputListApiView, OutputListApiView, logout_artemis, text2image, login_artemis
)

router = routers.DefaultRouter()
router.register("outputs", OutputListApiView)

urlpatterns = [
    path("", include(router.urls)),
    path("profiles", ProfileListApiView.as_view()),
    path("inputs/<int:user_id>", InputListApiView.as_view()),
    path("login", login_artemis),
    path("logout", logout_artemis),
    path("text2image", text2image),
]
