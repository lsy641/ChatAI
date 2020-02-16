from django.urls import path
from . import views
app_name = "chatai"
urlpatterns = [
	path('',views.index, name="index"),
	path('register/',views.register, name='register'),
	path('<int:room_id>/room/',views.room,name="room"),
	path('<int:room_id>/login/',views.login,name="login"),
	path('<int:room_id>/verify/',views.verify,name="verify"),
	path('<int:room_id>/close/',views.close,name="close"),
]
