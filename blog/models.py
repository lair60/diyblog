from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
# Create your models here.

		
class BlogAuthor(models.Model):
    user= models.OneToOneField(User,on_delete=models.SET_NULL, null= True)
    bio= models.CharField(max_length=100,help_text="Enter a bio about Blog Author")
	
    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('blogger-detail', args=[str(self.id)])
    
    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return self.user.username

class Blog(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the blog name")
    description = models.TextField(max_length=1000, help_text="Enter a description about blog")
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)
    post_date = models.DateField(null=True, blank=True)
    def __str__(self):
        """
        String que representa al objeto Book
        """
        return self.name
    
    
    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('blog-detail', args=[str(self.id)])
		
class BlogComment(models.Model):
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here")
    post_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, null=True)
    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return self.description
    class Meta:
        ordering = ["post_date"]
		
class TemporalLink(models.Model):
    link_temporal = models.CharField(max_length=100)
	
    email_request = models.CharField(max_length=100,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        """
        String que representa al objeto Book
        """
        return self.link_temporal