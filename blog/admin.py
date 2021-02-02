from django.contrib import admin

# Register your models here.
from .models import Blog, BlogAuthor, BlogComment, TemporalLink

# Define the admin class
@admin.register(TemporalLink) 
class TemporalLinkAdmin(admin.ModelAdmin):
    list_display = ('link_temporal', 'email_request' , 'created_at')
    fields = ['link_temporal', 'email_request']
	
	
admin.site.register(BlogAuthor)


class BlogCommentsInline(admin.TabularInline):
    model = BlogComment
    extra = 0
	
# Define the admin class
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date', 'description')
    fields = ['name', 'author', 'post_date', 'description']
    inlines = [BlogCommentsInline]
# Register the admin class with the associated model
admin.site.register(Blog, BlogAdmin)

@admin.register(BlogComment) 
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'post_date', 'description')
    fields = ['blog', 'author', 'description']
