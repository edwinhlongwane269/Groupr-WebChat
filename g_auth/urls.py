from django.urls import path, include, re_path
from g_auth.views import UserViewset, Login, Logout, TOTPCreateView, TOTPVerifyView, RefreshToken
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
router = DefaultRouter()
router.register(r'users$', UserViewset, basename="users")
auth_patterns = router.urls

createaccount = UserViewset.as_view({
    'post':'create',
     'get': 'list',
})


urlpatterns = [
    path("token/logout/", Logout.as_view(), name="logout"),
    path("token/", Login.as_view(), name="token"),
    path(
        "token/refresh/", RefreshToken.as_view(),
        name="token-refresh"
    ),
    path("enable_twofactor_auth/create/", TOTPCreateView.as_view(), name="totp-create"),
    re_path(r"^totp/login/(?P<token>[0-9]{6})/", TOTPVerifyView.as_view(), name="totp-login")
]


