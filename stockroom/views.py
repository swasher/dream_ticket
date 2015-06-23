# coding: utf-8
from django.shortcuts import redirect, render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.contrib import messages
from stockroom.models import Product, Like
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
            messages.add_message(request, messages.INFO, 'Wrong username or password')

    #return redirect('grid')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def logout(request):
    django_logout(request)
    return redirect('/')


def login_redirect(request):
    messages.add_message(request, messages.ERROR, 'You must be logged in for perform this operation')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def grid(request):
#     context_instance = RequestContext(request)
#     products = Product.objects.all()
#     return render_to_response('grid.html', {'products': products}, context_instance)


def grid(request):
    context_instance = RequestContext(request)
    product_list = Product.objects.all()

    # setup pagination for 3 item per page
    paginator = Paginator(product_list, 3)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    return render_to_response('grid.html', {'products': products}, context_instance)



def product(request, slug):
    context_instance = RequestContext(request)

    try:
        product = Product.objects.get(slug=slug)
    except product.DoesNotExist:
        raise Http404

    likes = Like.objects.filter(product=product)

    return render_to_response('product.html', {'product': product, 'likes': likes}, context_instance)

@login_required
def set_like(request, id):
    try:
        product = Product.objects.get(pk=id)
    except:
        raise Http404

    # if user already put like, database contain record with both product and user; so we send red message
    if Like.objects.filter(product=product, user=request.user).exists():
        messages.add_message(request, messages.ERROR, 'You already tap this button!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # create new 'like' record
    like = Like()
    like.user = request.user
    like.product = product
    like.save()
    messages.add_message(request, messages.SUCCESS, 'We are glad for your choice!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def add_comment(request, id):
    pass