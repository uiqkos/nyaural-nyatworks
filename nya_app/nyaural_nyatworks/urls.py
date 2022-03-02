from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from nya_app.nyaural_nyatworks import settings
from nya_app.nyaural_nyatworks.views import *

api_router = DefaultRouter()
api_router.register('reports', ReportViewSet)
api_router.register('models', ModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(api_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('predict/', CommentsView.as_view(), name='predict'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

