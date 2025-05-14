from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from deck.views import GetNextProfile
from user.views import ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/decks/<int:telegram_id>/', GetNextProfile.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
