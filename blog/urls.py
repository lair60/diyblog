from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^blogs/$', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    re_path(r'^bloggers/$', views.BloggerListView.as_view(), name='bloggers'),
    re_path(r'^blogger/(?P<pk>\d+)$', views.BloggerDetailView.as_view(), name='blogger-detail'),
	
	re_path(r'^newuser/$', views.SendLinkToRequestUser, name='new-user'),
	path('user/created/<str:valink>', views.createNewUser, name='new-user-details'),
	path('blog/<int:pk>/create/', views.BlogCommentCreate.as_view(), name='create-comment-post'),
	
]