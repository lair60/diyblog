from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blogs/$', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    url(r'^bloggers/$', views.BloggerListView.as_view(), name='bloggers'),
    url(r'^blogger/(?P<pk>\d+)$', views.BloggerDetailView.as_view(), name='blogger-detail'),
	
	url(r'^newuser/$', views.SendLinkToRequestUser, name='new-user'),
	path('user/created/<str:valink>', views.createNewUser, name='new-user-details'),
	path('blog/<int:pk>/create/', views.BlogCommentCreate.as_view(), name='create-comment-post'),
	
]