from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (EmailRegistrationView, RetrieveAccessToken, ReviewViewSet,
                    UserViewSet, CommentViewSet)

v1_router = SimpleRouter()
v1_router.register('users', UserViewSet, basename='auth-users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)


urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', EmailRegistrationView.as_view()),
    path(
        'auth/token/', RetrieveAccessToken.as_view(), name='token_obtain_pair'
    ),
]
