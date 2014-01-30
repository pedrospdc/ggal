from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from core.models import Picture


class PictureCreate(CreateView):
    success_url = reverse_lazy('picture-list')
    model = Picture
    fields = ['title', 'file']


class PictureUpdate(UpdateView):
    success_url = reverse_lazy('picture-list')
    model = Picture
    fields = ['title', 'file']


class PictureDelete(DeleteView):
    success_url = reverse_lazy('picture-list')
    model = Picture

    def post(self, request, *args, **kwargs):
        if request.POST['answer'] == 'Delete':
            return super(PictureDelete, self).post(request, *args, **kwargs)
        return HttpResponseRedirect(self.success_url)


class PictureList(ListView):
    model = Picture
