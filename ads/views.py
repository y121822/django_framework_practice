from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q

from ads.models import Ad, Comment, Fav
from ads.forms import CreateForm, CommentForm
from ads.owner import OwnerListView, OwnerDetailView, OwnerDeleteView


class AdListView(OwnerListView):
    model = Ad
    template_name = "ads/ad_list.html"

    def get(self, request):
        favorites, search, ad_list = [], request.GET.get("search", False), None

        if request.user.is_authenticated:
            favorites = [row['id'] for row in request.user.favorite_ads.values('id')]
        if search:
            query = Q(title__icontains=search) | Q(text__icontains=search) | Q(tags__name__in=[search])
            ad_list = Ad.objects.filter(query).distinct().select_related().order_by('-updated_at')[:10]

        else:
            ad_list = Ad.objects.all().order_by('-updated_at')[:10]

        if ad_list:
            for obj in ad_list:
                obj.natural_updated = naturaltime(obj.updated_at)

        return render(request, self.template_name, {'ad_list': ad_list, 'favorites': favorites})


class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/ad_detail.html"

    def get(self, request, pk):
        ad = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'ad': ad, 'comments': comments, 'comment_form': comment_form}
        return render(request, self.template_name, context)


class AdCreateView(LoginRequiredMixin, View):
    model = Ad
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy('ads:all')
    fields = ['title', 'text', 'price', 'tags']

    def get(self, request, pk=None):
        return render(request, self.template_name, {'form': CreateForm()})

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        form.save_m2m()

        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    model = Ad
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy('ads:all')
    fields = ['title', 'text', 'price']

    def get(self, request, pk):
        ctx = {'form': CreateForm(instance=get_object_or_404(Ad, id=pk, owner=self.request.user))}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        data = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=data)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad


def stream_file(request, pk):
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=ad)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/ad_comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        fav = Fav(user=request.user, ad=get_object_or_404(Ad, id=pk))
        try:
            fav.save()
        except IntegrityError:
            pass

        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            Fav.objects.get(user=request.user, ad=get_object_or_404(Ad, id=pk)).delete()
        except Fav.DoesNotExist:
            pass

        return HttpResponse()


