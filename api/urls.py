from django.urls import path
from .views import (
    EmployeeCreateView,
    EmployeeListView,
    EmployeeRetrieveView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    EmployeeFilterView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)

urlpatterns = [
    # Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Employee endpoints
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/<int:id>/', EmployeeRetrieveView.as_view(), name='employee-detail'),
    path('employees/<int:id>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:id>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),
     path('api/employees/filter/', EmployeeFilterView.as_view(), name='employee-filter'),
]