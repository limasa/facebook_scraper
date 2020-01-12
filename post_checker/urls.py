from django.urls import path
# from django.contrib.auth.decorators import login_required
from .views import LoginView, LogoutView, LandingPageView, SignUpView, add_link, main_view, my_pages, single_page_view, refresh_posts


urlpatterns = [
    path('', LandingPageView.as_view(), name='home'),
    path('submit/', add_link, name='link_submit'),
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('main/', main_view, name='main'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my_pages/', my_pages, name='my_pages'),
    path('my_pages/<int:pk>/',
         single_page_view, name='single_page_posts'),
    path('refresh_posts/<int:pk>/',
         refresh_posts, name='refresh_posts'),
]
