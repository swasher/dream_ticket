# coding: utf-8
from django.db.models import Count
from django.shortcuts import redirect, render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from stockroom.models import Product, Like, Comment
from .forms import CommentForm


def about(request):
    return render_to_response('about.html')


def login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        print 'username', username
        print 'pass', password
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
            else:
                #context['error'] = 'Non active user'
                messages.add_message(request, messages.INFO, 'Non active user')
        else:
            messages.add_message(request, messages.ERROR, 'Wrong username or password')

    #return redirect('grid')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def logout(request):
    django_logout(request)
    return redirect('/')


def login_redirect(request):
    messages.add_message(request, messages.ERROR, 'You must be logged in for perform this operation')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def grid(request):
    context_instance = RequestContext(request)

    # for security reasons we limit acceptable 'order_by'
    VALID_SORTS = {
        "name": "name",
        "price": "price",
        "-likes": "-likes",   # we want descent sort
    }
    DEFAULT_SORT = 'name'

    # Choose ordering column and pagination page
    page = request.GET.get('page', 1)
    get_order_by = request.GET.get('order_by', DEFAULT_SORT)
    order_by = VALID_SORTS.get(get_order_by, DEFAULT_SORT)

    # Count likes using 'annotate' feature. Then likes number will be accessible via product_list.likes
    product_list = Product.objects.all().annotate(likes=Count('like')).order_by(order_by)

    # setup pagination for 4 item per page
    paginator = Paginator(product_list, 4)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render_to_response('grid.html', {'products': products, 'order_by': order_by}, context_instance)


def product(request, slug):
    context_instance = RequestContext(request)

    # get appropriate "product" based on slug
    try:
        product = Product.objects.get(slug=slug)
    except product.DoesNotExist:
        raise Http404


    # form handler
    #
    # if user press 'submit', this branch run
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():

            # check if user if logged in
            if request.user.is_authenticated():
                # save comment to database
                user_comment = form.cleaned_data['user_comment']
                comment = Comment()
                comment.user = request.user
                comment.product = product
                comment.contents = user_comment
                comment.save()

                # finally, we clean form
                # form = CommentForm()

                # if a user hits “Refresh” on a page that was loaded via POST, that request will be repeated. http://www.djangobook.com/en/2.0/chapter07.html
                # so we need redirect
                messages.add_message(request, messages.SUCCESS, 'Comment successfully added!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                # if user not logged in, he can't live comments
                return redirect('login_redirect')

    # else we render empty form
    else:
        form = CommentForm()

    # Show users, who like this product
    likes = Like.objects.filter(product=product)

    # We show comment on product page
    comments = Comment.objects.filter(product=product).order_by('created_at').reverse

    return render_to_response('product.html', {'product': product, 'likes': likes, 'form': form, 'comments': comments}, context_instance)


@login_required
def set_like(request, id):
    try:
        product = Product.objects.get(pk=id)
    except:
        raise Http404

    # if user already put like, database contain record with both product and user; so we send red message
    if Like.objects.filter(product=product, user=request.user).exists():
        messages.add_message(request, messages.ERROR, 'You"ve clicked this button already!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # create new 'like' record
    like = Like()
    like.user = request.user
    like.product = product
    like.save()

    # return to previous page and conglaturate user
    messages.add_message(request, messages.SUCCESS, 'We are glad for your choice!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
