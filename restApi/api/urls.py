from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# register the ProfileDetailView to the router
router = DefaultRouter()
router.register(r"profile-actions", views.ProfilesViewActions, basename="profile_actions")
router.register(r"posts-actions",views.PostsSerializeView, basename="post")
router.register(r"user-profile", views.UserProfileFollowersActions, basename="user-action")
urlpatterns = [

    path('', views.UserProfileView.as_view(), name="profiles"),
    path('posts/', views.AllPostsView.as_view()),
    path('register/', views.RegisterUser.as_view()),
    # include the profile urls to the urls path
    path('', include(router.urls))

   
]


urlpatterns += [ path('api-auth/', include('rest_framework.urls'))]