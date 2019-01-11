from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView


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

