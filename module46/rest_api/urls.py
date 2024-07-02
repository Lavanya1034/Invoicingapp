from django.urls import path # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from .views import SignInView,SignUpView,InvoiceView,InvoiceDetailView,ItemsView

urlpatterns=[
   
    path("signup/",csrf_exempt(SignUpView.as_view()),name="sign_up"),
    path("login/",csrf_exempt(SignInView.as_view()),name="sign_in"),
    path("invoices/",csrf_exempt(InvoiceView.as_view()),name="get_invoice" ),
    path("invoices/new/",csrf_exempt(InvoiceView.as_view()),name="invoice_new_post" ),
    path("invoices/<int:id>/",csrf_exempt(InvoiceDetailView.as_view()),name="Invoice-Detail-View" ),
    path("invoices/<int:id>/items/",csrf_exempt(ItemsView.as_view()),name="add_items" ),
   
]   