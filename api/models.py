from django.db import models
# this class saves the employee information
class Employee(models.Model):
    name = models.CharField(max_length=255)  # saves name 
    email = models.EmailField(unique=True)    # saves email with unique email
    department = models.CharField(max_length=100, blank=True, null=True)  #saves which departement is it
    role = models.CharField(max_length=100, blank=True, null=True)       # role of employee  
    date_joined = models.DateField(auto_now_add=True)          # when he is joine means,when the user created and its automatically add when usr creates          

    def __str__(self):
        return f"{self.name} ({self.department})"
