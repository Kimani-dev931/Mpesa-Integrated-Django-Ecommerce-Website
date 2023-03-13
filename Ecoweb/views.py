from django.shortcuts import render, get_object_or_404
from .models import Item, OrderItem, Order
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from .models import Item, OrderItem, Order
from django.utils import timezone


# Create your views here.
def index(request):
    data = Item.objects.all()
    context = {
        'data': data
    }
    return render(request, "index.html", context)


def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            kim = Item.objects.filter(title__icontains=query)
            return render(request, 'index.html', {'kim': kim})
        else:
            print("No information to show")
            return render(request, 'index.html', {})


def detailitem(request):
    return render(request, "product-detail.html")


def cartlist(request):
    return render(request, "cart.html")


def checkout(request):
    return render(request, "checkout.html")


def complete(request):
    return render(request, "order-complete.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


class HomeView(ListView):
    model = Item
    template_name = "index.html"


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            message.error(self.request, "You do not have an active order")
            return redirect("/")


class ProductDetailView(DetailView):
    model = Item
    template_name = "product-detail.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("detail", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
            order.items.remove(order_item)
            return redirect("cart")
        else:
            # add a message saying the order does not contain the item
            return redirect("detail", slug=slug)
    else:
        # add a message saying the user doesn't have an order
        return redirect("detail", slug=slug)
    return redirect("detail", slug=slug)
