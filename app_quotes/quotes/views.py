from django.contrib.admin.templatetags.admin_list import paginator_number
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AuthorForm, QuoteForm
#from .utils import get_mongodb
from .models import Author, Quote, Tag


def main(request, page=1):
    # db = get_mongodb()
    # quotes = db.quotes.find()
    quotes = Quote.objects.all()
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, 'top_tags': top_tags})


def author_detail(request, author_id):
    author = get_object_or_404(Author, fullname=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})


@login_required
def author_add(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='/')
        else:
            return render(request, 'quotes/author_add.html', {'form': form})
    return render(request, 'quotes/author_add.html', {'form': AuthorForm()})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='/')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})


def quotes_by_tag(request, tag_name, page=1):
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.filter(tags=tag)
    per_page = 5
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/quotes_by_tag.html', {'quotes': quotes_on_page, 'tag': tag, 'top_tags': top_tags})
