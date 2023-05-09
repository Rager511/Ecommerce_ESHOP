from django.urls import path
from .views import index, detail, checkout, confirmation, register, user_login, user_logout, product_by_category, \
    payment,feedback_list
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('home/', index, name='home'),
    path('home/<int:myid>/', detail, name="detail"),
    path('checkout/', checkout, name="checkout"),
    path('confirmation/', confirmation, name="confirmation"),
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('category/<str:category_name>/', product_by_category, name='product_by_category'),
    path('payment/', payment, name='payment'),
    path('feedback/', feedback_list, name='feedback'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)