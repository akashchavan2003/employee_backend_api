from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'department', 'role', 'date_joined']

    def validate_name(self, value):
        if not value.strip():  # Ensure name is not empty
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    def validate_email(self, value):
        # Check if the email is already used by another employee
        employee_id = self.instance.id if self.instance else None
        if Employee.objects.exclude(id=employee_id).filter(email=value).exists():
            raise serializers.ValidationError("An employee with this email already exists.")
        return value