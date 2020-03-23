from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .apiviews import (
						ChoiceList,
						CreateVote,
						PollViewSet,
						)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls')

schema_view = get_schema_view(openapi.Info(title="Snippets API", default_version='v1',), public=True,)

urlpatterns = [
	path('polls/<int:pk>/choices/', ChoiceList.as_view(), name='choice_list'),
	path('polls/<int:pk>/choices/<int:choice_pk>/vote/', CreateVote.as_view(), name='create_vote'),

	#LogIn, LogOut, and password reset API endpoints
	path('', include('rest_auth.urls')),
	
	#Add LogIn, LogOut directly to the browsable API
	path('auth-api/', include('rest_framework.urls')),

	#Registration
	path('registration/', include('rest_auth.registration.urls')),

	#API Documentation
	url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls