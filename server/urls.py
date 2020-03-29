from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

#drf_yasg import
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

urlpatterns = []

urlpatterns += [
    path('admin/', admin.site.urls),
    path('', include('api.url')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

admin.site.site_header = 'Bolt&Nut 관리자 페이지'
admin.site.site_title = 'Bolt&Nut'

# drf_yasg 셋팅
schema_url_v1_patterns = [
    url('', include('api.url', namespace='boltnnut_api')),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="BOLTNNUT API",
        default_version='v1',
        description="볼트앤너트 API 문서.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rlqls505@naver.com"),
        license=openapi.License(name="Gibin Kwon"),
    ),
    validators=['flex'],  # 'ssv'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,
)

urlpatterns += [
        url('swagger(?P<format>\.json|\.yaml)/$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
        url('swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url('redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    ]

urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)