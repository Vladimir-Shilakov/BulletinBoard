from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Ads, Category, Reply, Author
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import AdsForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .signals import reply_notifications, send_message_reply_confirmed
from .filters import AdsFilter


class AdsList(ListView):
    model = Ads
    ordering = '-time_created'
    template_name = 'ads_list.html'
    context_object_name = 'ads_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AdsDetail(DetailView):
    model = Ads
    template_name = 'ads_detail.html'
    context_object_name = 'ads'
    queryset = Ads.objects.all()


class AdsCreate(CreateView, LoginRequiredMixin):
    model = Ads
    form_class = AdsForm
    template_name = 'ads_create.html'
    context_object_name = 'ads_create'

    def form_valid(self, form):
        user = self.request.user
        try:
            author = Author.objects.get(user=user)
        except Author.DoesNotExist:
            author = Author.objects.create(user=user)
        ads = form.save(commit=False)
        ads.author = author
        ads.save()
        return super().form_valid(form)


class AdsUpdate(UpdateView, LoginRequiredMixin):
    model = Ads
    form_class = AdsForm
    template_name = 'ads_edit.html'


class CategoryList(ListView):
    model = Ads
    template_name = 'category_list.html'
    context_object_name = 'category_ads_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Ads.objects.filter(category=self.category).order_by('-time_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


class Replies(ListView, LoginRequiredMixin):
    model = Reply
    template_name = 'my_replies.html'
    context_object_name = 'replies'
    paginate_by = 5

    def get_queryset(self):
        post = get_object_or_404(Ads, pk=self.kwargs['pk'])
        return post.replies.all()

    def get_queryset(self):
        self.queryset = Reply.objects.filter(ads__author__user_id=self.request.user.id)
        return super().get_queryset()


class ReplyCreate(CreateView, LoginRequiredMixin):
    model = Reply
    form_class = ReplyForm
    template_name = 'reply_create.html'
    context_object_name = 'reply_create'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.sender = self.request.user
        reply.ads = get_object_or_404(Ads, id=self.kwargs['pk'])
        author = reply.ads.author.user.email
        reply_notifications(author)
        form.save()
        return redirect('/')


class ReplyDelete(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('my_replies')


def reply_confirmed(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.confirmed = True
    sender = reply.sender.email
    reply.save()
    send_message_reply_confirmed(sender)
    return redirect('/replies/')


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'Вы отписались : '
    return render(request, 'subscribe.html', {'category': category, 'message': message})



