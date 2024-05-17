from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# register the ProfileDetailView to the router
router = DefaultRouter()
router.register(r"profile", views.ProfileDetialView)
router.register(r"profilefollow", views.FollowProfilesView, basename="profile_actions")

urlpatterns = [
    path('', views.UserProfileView.as_view(), name="profiles"),
    path('register/', views.RegisterUser.as_view()),
    # include the profile urls to the urls path
    path('', include(router.urls))

   
]


urlpatterns += [ path('api-auth/', include('rest_framework.urls'))]