from django.urls import path

from . import views


app_name = 'controls'
urlpatterns = [
    # SYSTEM FUNCTIONS.
    path('dashboard/signin/', views.dashboard_signin, name='signin'),
    path('dashboard/logout/', views.dashboard_logout, name='logout'),
    path('dashboard/change-password/', views.dashboard_password, name='change-password'),
    # DASHBOARD PAGE.
    path('dashboard/employee/', views.dashboard_employee, name='employee'),
    path('dashboard/product/', views.dashboard_product, name='product'),
    path('dashboard/reservation/', views.dashboard_reservation, name='reservation'),
    path('dashboard/importation/', views.dashboard_importation, name='importation'),
    path('dashboard/order/', views.dashboard_order, name='order'),
    # EMPLOYEE.
    path('dashboard/employee/create/', views.create_employee, name='create-employee'),
    path('dashboard/employee/update/<int:pk>', views.update_employee, name='update-employee'),
    # PRODUCT.
    path('dashboard/specification/create/', views.create_specification, name='create-specification'),
    path('dashboard/product/create/', views.create_product, name='create-product'),
    path('dashboard/product/update/<int:pk>', views.update_product, name='update-product'),
    path('dashboard/product/delete/<int:pk>', views.delete_product, name='delete-product'),
    # RESERVATION.
    path('dashboard/reservation/create/', views.create_reservation, name='create-reservation'),
    path('dashboard/reservation/view/<int:pk>', views.view_reservation, name='view-reservation'),
    path('dashboard/reservation/update/<int:pk>', views.update_reservation, name='update-reservation'),
    path('dashboard/reservation/delete/<int:pk>', views.delete_reservation, name='delete-reservation'),
    # IMPORTATION.
    path('dashboard/importation/create/', views.create_importation, name='create-importation'),
    path('dashboard/importation/view/<int:pk>', views.view_importation, name='view-importation'),
    # ORDER.
    path('dahsboard/order/view/<int:pk>', views.view_order, name='view-order'),
    path('dahsboard/order/confirm/<int:pk>', views.confirm_order, name='confirm-order'),
    path('dahsboard/order/deliver/<int:pk>', views.deliver_order, name='deliver-order')
]
