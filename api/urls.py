from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from .views import (
    ProfileListApiView, InputListApiView, OutputListApiView,
    logout_artemis, text2image, login_artemis, get_csrf_token, post_processing, signup_artemis, get_logged_in_user, get_public_outputs
)

router = routers.DefaultRouter()
router.register("outputs", OutputListApiView)

urlpatterns = [
    path("", include(router.urls)),
    path("profiles", ProfileListApiView.as_view()),
    path("inputs/<int:user_id>", InputListApiView.as_view()),
    path("login", login_artemis),
    path("logout", logout_artemis),
    path("signup", signup_artemis),
    path("text2image", text2image),
    path("csrf", get_csrf_token),
    path("post-processing", post_processing),
    path("logged-in-user", get_logged_in_user),
    path("public-outputs", get_public_outputs),
]
