from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.views.generic import ListView, DetailView, CreateView


# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html')


'''
Class based views - generic views for different, generic functionalities
    -different types (update, list, detail views, etc)
    -Use a template with the following naming pattern by default:
        <app>/<model>_<viewtype>.html
'''


# Class based view for the home page
class PostListView(ListView):           # inherit from ListView
    model = Post                        # Set the model to be queried for list
    # change the name of the default template used by the ListView
    template_name = 'blog/home.html'    # default template: <app>/<model><viewtype>.html
    # set an attribute to rename the object to be presented in a list
    context_object_name = 'posts'       # default var: object_list
    # order by inverse date_posted
    ordering = ['-date_posted']


# Class based view for the post page (details)
class PostDetailView(DetailView):           # inherit from ListView
    model = Post                        # Set the model to be queried for list


# Class based view to create a new post
class PostCreateView(LoginRequiredMixin, CreateView):           # inherit from ListView
    model = Post                        # Set the model to be queried for list
    # This view includes a form - we must set the fields in that form
    fields = ['title', 'content']
    # default template name is different from normal format because the template is shared
    # with the UpdateView. The name for this template should be:
    #   <app>/<model>_form.html

    # we need to override the form_valid method to store the author when a post form is submitted
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Last requirement for a CreateView is to provide a redirect url or an absolute url to a specific
    # model instance
    # success_url = 'blog-home'
