from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError

# Pagination class
class EmployeePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# View to create a new employee
class EmployeeCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handle POST requests to create a new employee."""
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to retrieve a single employee by ID
class EmployeeRetrieveView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        """Retrieve an employee object by ID."""
        try:
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found.")

    def get(self, request, id):
        """Handle GET requests to retrieve a single employee."""
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

# View to update an employee
class EmployeeUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        """Retrieve an employee object by ID."""
        try:
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found.")

    def put(self, request, id):
        """Handle PUT requests to update an employee (full update)."""
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        """Handle PATCH requests to update an employee (partial update)."""
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeFilterView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        # Retrieve query parameters
        department = request.query_params.get('department')
        role = request.query_params.get('role')

        # Start with all employees
        queryset = Employee.objects.all()

        # Validate and filter by department if provided
        if department:
            if not Employee.objects.filter(department=department).exists():
                raise ValidationError("No department found.")
            queryset = queryset.filter(department=department)

        # Validate and filter by role if provided
        if role:
            if not Employee.objects.filter(role=role).exists():
                raise ValidationError("Invalid role.")
            queryset = queryset.filter(role=role)

        # Serialize filtered queryset
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# View to delete an employee
class EmployeeDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        """Retrieve an employee object by ID."""
        try:
            return Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            raise NotFound("Employee not found.")

    def delete(self, request, id):
        """Handle DELETE requests to delete an employee."""
        employee = self.get_object(id)
        employee.delete()
        return Response({"message": "Employee deleted successfully."}, status=status.HTTP_200_OK)

# View to list employees with filtering and pagination
class EmployeeListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Handle GET requests to list employees with filtering and pagination."""
        department = request.query_params.get('department', None)
        role = request.query_params.get('role', None)

        # Filter employees based on department and role
        employees = Employee.objects.all()
        if department:
            employees = employees.filter(department=department)
        if role:
            employees = employees.filter(role=role)

        # Pagination
        paginator = EmployeePagination()
        paginated_employees = paginator.paginate_queryset(employees, request)
        serializer = EmployeeSerializer(paginated_employees, many=True)
        return paginator.get_paginated_response(serializer.data)