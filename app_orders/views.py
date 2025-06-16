from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class OrderView(TemplateView):
    """Отображение корзины"""
    template_name = 'app_cart/cart_detail.html'
    # form = CartAddProductForm()

    def post(self, request, *args, **kwargs):
        # remove_from_cart(request)
        print(request.POST)
        return render(request,self.template_name,context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['cart'] = get_cart(self.request)
        context['form'] = self.form
        return context
