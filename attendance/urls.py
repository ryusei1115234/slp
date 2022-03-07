from django.urls import path
from . import views

urlpatterns =[
    path("create",views.create,name='create'),
    path("record",views.record,name='record'),
    path("start_end",views.start_end,name='start_end'),
    path("rest",views.rest,name='rest'),
    path("login",views.Login,name='Login'),
    path("history",views.history,name='history'),
    path("edit/<int:num>",views.edit,name='edit'),
    path("pay_edit/<int:num>",views.pay_edit,name='pay_edit'),
    path("payment",views.payment,name='payment'),
    path("new_staff",views.new_staff,name='new_staff'),
]