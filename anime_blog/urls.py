from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from main.views import PostViewset, CommentViewset, LikeViewset, RatingViewset

from rest_framework import permissions

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from main.views import PostFavouriteView, ParsingView



schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('posts', PostViewset)
router.register('likes', LikeViewset)
router.register('comments', CommentViewset)
router.register('ratings', RatingViewset)

urlpatterns = [
    path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/favourites/', PostFavouriteView.as_view()),
    path('api/v1/news/', ParsingView.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
