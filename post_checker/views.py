from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
import random
from django.contrib.auth.decorators import login_required
from .models import Page, Post
from .forms import UserRegisterForm, LinkSubmitForm, WordSearchForm

from . import scrape


class SignUpView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'sign_up.html'


class LandingPageView(TemplateView):
    template_name = 'home.html'


class LoginView(LoginView):
    template_name = 'login.html'
    success_url = 'main.html'


class LogoutView(LogoutView):
    success_url = 'home.html'


@login_required
def my_pages(request):

    context = {
        'pages': Page.objects.filter(user_id=request.user.id)

    }

    return render(request, 'my_pages.html', context)


@login_required
def main_view(request):
    form = WordSearchForm(request.POST)
    if request.method == 'POST':
        form = WordSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['word']

            context = {
                'post_list': Post.objects.filter(page__user=request.user, post_text__contains=data).order_by('-post_id')
            }
            return render(request, 'posts_new.html', context)

    posts_query = Post.objects.filter(
        page__user=request.user).order_by('-post_id')

    # rand_posts = random.choices(posts_query, k=12)
    context = {

        'post_list':  posts_query,
        'form': form
    }
    return render(request, 'main.html', context)


@login_required
def single_page_view(request, pk):

    context = {

        'post_list': Post.objects.filter(page__user=request.user, page_id=pk),
        'page_name': Page.objects.get(user=request.user, id=pk)

    }

    return render(request, 'single_page_posts.html', context)


@login_required
def refresh_posts(request, pk):
    data = Page.objects.get(id=pk)
    link = data.general_link

    post_data = scrape.get_data(link)
    page_name = scrape.page_name(link)
    post_time = scrape.get_time(link)
    page_img_link = scrape.page_img_link(link)
    page_id = scrape.page_id(link)

    page = Page(user=request.user, page_identifier=page_id, page_author=page_name,
                general_link=data, page_img_link=page_img_link)
    if Page.objects.filter(user=request.user, page_identifier=page_id).exists():
        pass
    else:
        page.save()

    for post_id, time in zip(post_data.keys(), post_time.keys()):

        if Post.objects.filter(page__user=request.user).filter(post_id=post_id).exists():
            pass
        else:
            post = Post(page=Page.objects.get(user=request.user, page_identifier=page_id), post_author=page_name,
                        post_text=post_data[post_id], post_id=post_id, post_time=post_time[time],)

            post.save()

    context = {

        'post_list': Post.objects.filter(
            page__user=request.user, page_id=pk).order_by('-post_id'),
        'page_name': Page.objects.get(id=pk)

    }

    return render(request, 'single_page_posts.html', context)


data = ''


@login_required
def add_link(request):
    form = LinkSubmitForm(request.POST)
    if request.method == 'POST':
        form = LinkSubmitForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['general_link']
            post_data = scrape.get_data(data)
            page_name = scrape.page_name(data)
            post_time = scrape.get_time(data)
            page_img_link = scrape.page_img_link(data)
            page_id = scrape.page_id(data)

            page = Page(user=request.user, page_identifier=page_id, page_author=page_name,
                        general_link=data, page_img_link=page_img_link)
            if Page.objects.filter(user=request.user, page_identifier=page_id).exists():
                pass
            else:
                page.save()

            for post_id, time in zip(post_data.keys(), post_time.keys()):

                if Post.objects.filter(page__user=request.user).filter(post_id=post_id).exists():
                    pass
                else:
                    post = Post(page=Page.objects.get(user=request.user, page_identifier=page_id), post_author=page_name,
                                post_text=post_data[post_id], post_id=post_id, post_time=post_time[time],)

                    post.save()

            context = {

                'post_list': Post.objects.filter(page__user=request.user, post_author=page_name).order_by('-post_id'),
                'page_name': Page.objects.get(user=request.user, page_identifier=page_id)

            }

            return render(request, 'posts_new.html', context)

    return render(request, 'link_submit.html', {'form': form})
