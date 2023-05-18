from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Blog, BlogAuthor, BlogComment, TemporalLink
from django.views.generic.edit import CreateView
from blog.forms import CreateNewUserForm
from django.contrib.auth.models import User
import secrets
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django.core.mail import EmailMessage
from django.urls import reverse

def SendLinkToRequestUser(request):
    context = {}
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = CreateNewUserForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            email_user = form.cleaned_data['email_user']		
            if User.objects.filter(email=email_user).count() == 0:
                if TemporalLink.objects.filter(email_request=email_user).count() == 0:
                    if request.is_secure():
                        url= "https://"
                    else:
                        url= "http://"
                    link_value =  secrets.token_urlsafe()
                    link_obj = TemporalLink(link_temporal=link_value, email_request=email_user)
                    link_obj.save()
                    context = {'email': email_user}
                    url= url + request.get_host() + reverse ('new-user-details',args=[link_value])
			
                    message_email_html = (f'<p><b>Hello</b>,</p><br>'
                                       f'<p>Thank you for your request. Please click on the following link to validate the request and create the new user details:</p><br>'                                       
                                       f"""<p><a href=\'{url}\' target='_blank'>{url}</a></p>"""
                                       f'<p>If you have questions or comments please email me anytime at <a href="mailto:lair60@yahoo.es" target="_blank">lair60@yahoo.es</a>.</p>'
                                       f'<p>Best regards,</p>'
                                       f'<p>Luis Inga</p>'
                                       f'<p><a href="https://www.luisingarivera.online" target="_blank">https://www.luisingarivera.online</a></p>')
                    msg = EmailMessage('Validate your request', message_email_html, 'lair60@yahoo.es', [email_user])
                
                    msg.content_subtype = "html"
                    msg.send()
                else:
                    context = {'link_sent_already': True}
                return render(request, 'blog/link_created.html', context)	
            return render(request, 'blog/link_created.html', context)		
    else:
        template_name ='blog/create_user_form.html'
        form = CreateNewUserForm()
        context = {'form': form}
        return render(request, 'blog/create_user_form.html', context)


def createNewUser(request,valink):
    context = {}
    if request.method == 'GET':              
        # Create a form instance and populate it with data from the request (binding):
        temp_obj = TemporalLink.objects.filter(link_temporal=valink)
        if temp_obj.count() == 1:
            obj_link = temp_obj[0]
        #form = CreateNewUserForm(request.POST)

        # Check if the form is valid:
        #if form.is_valid():
            #email_user = form.cleaned_data['email_user']
            email_user = obj_link.email_request
            if User.objects.filter(email=email_user).count() == 0:
                # redirect to a new URL:
                context = {'email': email_user}                
                password = secrets.token_urlsafe(16)             
                user = User.objects.create_user(email_user, email_user, password)
                if request.is_secure():
                    url= "https://"
                else:
                    url= "http://"
                url= url + request.get_host() + reverse ('login')
				
                message_email_html = (f'<p><b>Hello</b>,</p><br>'
                                       f'<p>As per your request, here are the details of the new user:</p><br>'
                                       f'<p>       <b>Username</b>: {email_user}</p>'
                                       f'<p>       <b>Password</b>: {password}</p><br>'
                                       f"""<p>To log in, visit <a href=\'{url}\' target='_blank'>{url}</a> and enter in your username and password.</p>"""
                                       f'<p>If you have questions or comments please email me anytime at <a href="mailto:lair60@yahoo.es" target="_blank">lair60@yahoo.es</a>.</p>'
                                       f'<p>Thanks!</p>'
                                       f'<p>Luis Inga</p>'
                                       f'<p><a href="https://www.luisingarivera.online" target="_blank">https://www.luisingarivera.online</a></p>')
                msg = EmailMessage('Your new user details', message_email_html, 'lair60@yahoo.es', [email_user])
                """
                send_mail(
                    'User Created',
                    'Username: '+ email_user + ' password: '+ password,
                    'lair60@yahoo.es',
                    [email_user],
                    fail_silently=False,
                )
				"""
                msg.content_subtype = "html"
                msg.send()
        return render(request, 'blog/user_created.html', context)

# Create your views here.
def index(request):
    num_blogs=Blog.objects.all().count()
    num_authors=BlogAuthor.objects.all().count()
    num_comments=BlogComment.objects.all().count()
    #search_word='the'
    #num_blog_search = Blog.objects.filter(name__icontains=search_word).count()
	
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    return render(
        request,
        'index.html',
        context={'num_blogs': num_blogs, 'num_authors': num_authors, 'num_comments': num_comments,'num_visits': num_visits}
       )

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
class BlogListView(generic.ListView):
    model = Blog
    context_object_name = 'blog_list'   # your own name for the list as a template variable
    template_name ='blog/blog_list.html'
    paginate_by = 10
	
class BloggerListView(generic.ListView):
    model = BlogAuthor
    context_object_name = 'blogger_list'   # your own name for the list as a template variable
    template_name ='blog/blogger_list.html'
    paginate_by = 10

class BloggerDetailView(generic.ListView):
    model = Blog
    paginate_by = 10
    template_name ='blog/blog_list_blogger_detail.html'
    def get_queryset(self):
        """
        We get the list of books of the author in the variable blog_list
        """
        author = get_object_or_404(BlogAuthor, pk = self.kwargs['pk'])
        return Blog.objects.filter(author=author)
		
    def get_context_data(self, **kwargs):
        context = super(BloggerDetailView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk"
        context['blogger'] = get_object_or_404(BlogAuthor, pk = self.kwargs['pk'])
        return context

class BlogDetailView(generic.DetailView):
    model = Blog
	
class BlogCommentCreate(LoginRequiredMixin, CreateView):
    model = BlogComment
    fields = ['description']
	
    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        #Add logged-in user as author of comment
        form.instance.author = self.request.user
        #Associate comment with blog based on passed id
        form.instance.blog=get_object_or_404(Blog, pk = self.kwargs['pk'])
        # Call super-class form validation behavior
        return super(BlogCommentCreate, self).form_valid(form)
	
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context
		
    def get_success_url(self): 
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})