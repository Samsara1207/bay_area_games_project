"""
URL configuration for bay_area_games project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 前端页面
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teams/', views.teams, name='teams'),
    path('athletes/', views.athletes, name='athletes'),
    path('events/', views.events, name='events'),
    path('referees/', views.referees, name='referees'),
    path('sponsors/', views.sponsors, name='sponsors'),
    path('logistics/', views.logistics, name='logistics'),
    path('results/', views.results, name='results'),
    path('statistics/', views.statistics, name='statistics'),
    # API接口
    path('api/basic/', include('basic_info.urls')),
    path('api/events/', include('event_management.urls')),
    path('api/referees/', include('referee_management.urls')),
    path('api/results/', include('result_management.urls')),
    path('api/logistics/', include('logistics.urls')),
    path('api/operations/', include('operation.urls')),
    path('api/appeals/', include('appeal_arbitration.urls')),
    path('api/business/', include('business.urls')),
    path('api/finance/', include('finance_safety.urls')),
    path('api/statistics/', include('data_statistics.urls')),
]
