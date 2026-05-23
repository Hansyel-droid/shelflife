from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),   # Google login routes
    path('api/v1/', include('pantry.urls')),
    path('', login_required(TemplateView.as_view(template_name='pantry/index.html')), name='home'),
]
