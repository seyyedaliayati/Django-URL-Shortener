from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin

from .misc import (hash_encode,
                   get_absolute_short_url,
                   process_new_click)
from .forms import URLShortenerForm
from .models import Link


class NewLinkView(LoginRequiredMixin, FormView):
    template_name = 'app_urls/index.html'
    form_class = URLShortenerForm

    def form_valid(self, form):
        request = self.request
        original_alias = form.cleaned_data['alias']
        alias = original_alias.lower()
        url = form.cleaned_data['url']
        new_link = Link(user=request.user, url=url)
        try:
            latest_link = Link.objects.latest('id')
            if Link.objects.filter(alias__exact=alias).exists():
                # handle alias conflict
                new_link.alias = alias + '-' + hash_encode(latest_link.id+1)
                messages.add_message(request, messages.INFO,
                                     'Short URL {} already exists so a new short URL was created.'
                                     .format(get_absolute_short_url(request, original_alias)))
                original_alias = new_link.alias
            else:
                new_link.alias = alias or hash_encode(latest_link.id+1)
        except Link.DoesNotExist:
            new_link.alias = alias or hash_encode(1)
        new_link.save()
        return HttpResponseRedirect(reverse('app_urls:preview', args=(original_alias or new_link.alias,)))


class LinkPreview(LoginRequiredMixin, DetailView):
    model = Link
    template_name = 'app_urls/preview.html'
    slug_url_kwarg = 'alias'
    slug_field = 'alias__iexact'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context.update({
            'alias': obj.alias,
            'absolute_short_url': get_absolute_short_url(self.request, obj.alias, remove_schema=False),
            'url': obj.url,
        })
        return context


class DeleteLinkView(LoginRequiredMixin, DeleteView):
    model = Link
    slug_url_kwarg = 'alias'
    slug_field = 'alias__iexact'
    success_url = reverse_lazy('app_urls:analytics')

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)


class LinkRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        alias = kwargs.get('alias', '')
        extra = kwargs.get('extra', '')
        link = get_object_or_404(Link, alias__iexact=alias)
        process_new_click(self.request, link)
        return link.url + extra


class AnalyticsView(LoginRequiredMixin, ListView):
    model = Link
    paginate_by = 10
    context_object_name = 'links'
    template_name = 'app_urls/analytics.html'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)
