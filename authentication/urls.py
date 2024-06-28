from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index , name='index'),
    path('register/', views.register, name='register' ),
    path('login/', views.login, name='login' ),
    path('userdashboard/', views.dashboard, name='dashbaord' ),
    path('logout/', views.signout, name='signout' ),
    path('matchedphotos/', views.matched_photos, name='matchedphotos' ),
    path('unmatchedphotos/', views.unmatched_photos, name='unmatchedphotos' ),
    path('allphotos/', views.all_photos, name='all_photos' ),
    path('upload_person/', views.upload_person, name='upload_person' ),
    path('admindashboard/', views.administ, name='administ' ),
    path('myusers',views.load_users,name = 'load_users'),
    path('generate',views.generate,name = 'generate'),
    path('changepwd',views.changepwd,name = 'generate')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)