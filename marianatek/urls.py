from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers

from movies.views import GenreViewSet
from movies.views import MovieViewSet

router = routers.DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'movies', MovieViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
