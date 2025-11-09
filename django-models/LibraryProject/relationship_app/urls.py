# relationship_app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # ✅ لازم السطر ده موجود حرفيًا

# relationship_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'relationship_app'

urlpatterns = [
    path('', views.list_books, name='home'),
    path('books/', views.list_books, name='list_books'),
    # role-based
    path('role/admin/', views.admin_view, name='admin_view'),
    path('role/librarian/', views.librarian_view, name='librarian_view'),
    path('role/member/', views.member_view, name='member_view'),

    # auth (login/logout/register) — افتراض أنك قد بنيت register view سابقًا
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),  # إذا لديك register() كما في السابق
]
