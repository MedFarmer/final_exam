from typing import Any
from django.db.models.query import QuerySet
from django.http import  HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, View, ListView, UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from .models import Rubric, Post, Comment
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

""" Ниже представления связанные с регистрацией, вход, выход, запрос на изменения пароля, подтверждения почты """

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def send_verify_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}')
        message = f'Здравствуйте, {user.username}! Перейдите по ссылке ниже для подтверждения почты:\n\n{verify_url}'
        send_mail('Подтверждение почты', message, 'medet20231020@gmail.com', [user.email])
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object        
        user.is_active = False
        user.save()
        self.send_verify_email(user)
        return response
    
class VerificationSuccess(TemplateView):
    template_name = 'verification_success.html'

class VerificationError(TemplateView):
    template_name = 'verification_error.html'

class VerifyEmailView(View):
    def get(self, request, user_id, token):
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verify_success')
        else:
            return redirect('verify_error')

class Login(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')

    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(password=password,username=username)
        if user is not None and user.is_active:
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(reverse_lazy('login')+'?active=false')
        
class Logout(LogoutView):    
    next_page = 'login'

    """
        Начальная страница отражающая имеющиеся рубрики
    """
class Home(ListView):
    model = Rubric
    template_name = 'home.html'
    context_object_name = 'rubrics'

    """
    Ниже представление на добавление поста. 

    """

class AddPost(View):    
    def get(self, request):
        form= AddPostForm()
        subrubrics = Rubric.objects.filter(parent__isnull=False)
        context = {'form': form, 'subrubrics':subrubrics}
        return render(request, 'addpost.html', context)
    
    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            rubric = form.cleaned_data['rubric']
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            price = form.cleaned_data['price']
            contact = form.cleaned_data['contact']
            image = form.cleaned_data['image']
            author = User.objects.get(id=request.user.id)
            rubric_query = Rubric.objects.get(name=rubric)
            Post.objects.create(rubric=rubric_query, title=title, content=content, price=price, contact=contact, image=image, author=author)
            return redirect('home')
        else:           
            context= {'form':form}
            return render(request, 'addpost.html', context)

"""
    Ниже представление на вывод перечня постов при входе в отдельную рубрику
"""

class PostsView(View):
    def get(self, request, subrubric_pk):
        rubric = Rubric.objects.get(pk=subrubric_pk)
        posts = Post.objects.filter(rubric=rubric)        
        
        paginator = Paginator(posts, 4)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        posts = paginator.get_page(page_num)
        
        context = {'page':posts}
        return render(request, 'posts.html', context)

"""
    Ниже представление на вывод отдельного объявления, с комментариями к данному посту. Форма для добавления комментариев. 
"""

class PostView(View):
    def post(self, request, subrubric_pk, post_pk):
        form = AddCommentForm(request.POST)
        post=Post.objects.get(pk=post_pk)
        
        if form.is_valid():
            content = form.cleaned_data['content']
            author = User.objects.get(pk=request.user.id)
            Comment.objects.create(post=post, author=author, content=content)
            return redirect(reverse('post', args=[subrubric_pk, post_pk]))
        else:           
            comments = Comment.objects.filter(post=post)
            context = {'form':form, 'comments':comments, 'post':post}
            return render(request, 'post.html', context)
        
    def get(self, request, subrubric_pk, post_pk):
        form = AddCommentForm(request.POST)
        post = Post.objects.get(pk=post_pk)
        comments = Comment.objects.filter(post=post)
        context = {'form':form, 'post':post, 'comments':comments}
        return render(request, 'post.html', context)

""" 
    Ниже представление на удаление комментария к посту. Комментарий может быть удален только тем кто создал комментарий
"""

class DeleteComment(View):
    def post(self, request, subrubric_pk, post_pk, comment_pk):        
        Comment.objects.get(pk=comment_pk).delete()
        return redirect(reverse('post', args=[subrubric_pk, post_pk]))
        
    def get(self, request, subrubric_pk, post_pk, comment_pk):
        comments = Comment.objects.get(pk=comment_pk)
        context = {'comments':comments}
        return render(request, 'delete_comment.html', context)
    
""" 
    Ниже представление на удаление объявления. Объявление может быть удалено только тем кто создал его.
"""
class DeletePost(View):
    def post(self, request, subrubric_pk, post_pk):
        Post.objects.get(pk=post_pk).delete()
        return redirect(reverse('posts', args=[subrubric_pk]))
        
    def get(self, request, subrubric_pk, post_pk,):
        posts = Post.objects.get(pk=post_pk)
        context = {'posts':posts}
        return render(request, 'delete_post.html', context)

"""
    Внесение изменений в объявление
"""

class UpdatePost(View):
    def post(self, request, subrubric_pk, post_pk):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():            
            post = Post.objects.get(pk=post_pk)
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.price = form.cleaned_data['price']
            post.contact = form.cleaned_data['contact']
            post.image = form.cleaned_data['image']
            post.save()
        
        return redirect(reverse('post', args=[subrubric_pk, post_pk]))
        
    def get(self, request, subrubric_pk, post_pk):
        form = AddPostForm(request.POST, request.FILES)
        post = Post.objects.get(pk=post_pk)
        context = {'form':form, 'post':post}
        return render(request, 'update_post.html', context)

