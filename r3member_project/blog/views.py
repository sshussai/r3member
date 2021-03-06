from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


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
    # pagination
    paginate_by = 5


# Class based view for posts from a specific user
class UserPostListView(ListView):           # inherit from ListView
    model = Post                        # Set the model to be queried for list
    # change the name of the default template used by the ListView
    template_name = 'blog/user_posts.html'    # default template: <app>/<model><viewtype>.html
    # set an attribute to rename the object to be presented in a list
    context_object_name = 'posts'       # default var: object_list
    # order by inverse date_posted
    # ordering = ['-date_posted'] -- cannot use this since the query is getting overridden
    # pagination
    paginate_by = 5

    # Change the queryset to get posts from a specific user, instead of all the posts
    def get_queryset(self):
        # this will get the user with the username that is gonna come from the url
        # and the get_object_or_404 will get the user if it exists or return 404
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # get the posts by that user, and order the returning set
        return Post.objects.filter(author=user).order_by('-date_posted')


# Class based view for the post page (details)
class PostDetailView(DetailView):           # inherit from ListView
    model = Post                        # Set the model to be queried for list


# Class based view to create a new post
class PostCreateView(LoginRequiredMixin, CreateView):           # inherit from ListView
    model = Post                        # Set the model to be queried for list
    # This view includes a form - we must set the fields in that form
    fields = ['title',  'code', 'content']
    # default template name is different from normal format because the template is shared
    # with the UpdateView. The name for this template should be:
    #   <app>/<model>_form.html

    def get_form(self, form_class=None):
        form = super(PostCreateView, self).get_form(form_class)
        form.fields['code'].required = False
        return form

    # we need to override the form_valid method to store the author when a post form is submitted
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Last requirement for a CreateView is to provide a redirect url or an absolute url to a specific
    # model instance
    # success_url = 'blog-home'


# Class based view to update post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):           # inherit from ListView
    model = Post                        # Set the model to be queried for list
    # This view includes a form - we must set the fields in that form
    fields = ['title', 'content', 'code']
    # default template name is different from normal format because the template is shared
    # with the CreateView. The name for this template should be:
    #   <app>/<model>_form.html

    def get_form(self, form_class=None):
        form = super(PostUpdateView, self).get_form(form_class)
        form.fields['code'].required = False
        return form

    # we need to override the form_valid method to store the author when a post form is submitted
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Last requirement for a UpdateView is to provide a redirect url or an absolute url to a specific
    # model instance
    # success_url = 'blog-home'

    # We have to make the sure that not only is a user logged in, but the user is the author of the post
    # he's trying to edit. So the UserPassesTestMixin which uses the this test_func will ensure that
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Class based view for the post page (details)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):           # inherit from DeleteView
    model = Post                        # Set the model to be queried for list

    # This method provides a form to base template asking the user if they're sure they wanna delete
    # So, the template name is: <app>/<model>_confirm_delete.html

    # We have to make the sure that not only is a user logged in, but the user is the author of the post
    # he's trying to edit. So the UserPassesTestMixin which uses the this test_func will ensure that
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    # For the delete view, we HAVE to provide a success_url
    success_url = '/'
