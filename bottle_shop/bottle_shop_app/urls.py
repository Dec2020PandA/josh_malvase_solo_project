from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_reg),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('bottle_shop_dash', views.bottle_shop_dash),
    path('post_message', views.post_message),
    path('mess_delete/<int:mess_id>', views.mess_delete),
    path('like/<int:message_id>', views.like_message),
    path('create_comment', views.create_comment),
    path('comm_delete/<int:comm_id>', views.comm_delete),
    path('profile/<int:user_id>', views.profile),
    path('my_profile/<int:user_id>', views.my_profile),
    path('edit_profile/<int:user_id>', views.edit_profile),
    # path('upload_prof_photo', views.upload_prof_photo),
    path('update/<int:user_id>', views.update_profile),
    path('add_bottle', views.add_bottle),
    # path('upload_bottle', views.upload_bottle),
 ]