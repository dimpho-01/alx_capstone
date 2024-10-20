from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Task(models.Model):
    """
    Model representing a task.
    """

    # Constants
    PRIORITY_LEVELS = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    )
    
    # Fields
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=15, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Validators
    def _validate_due_date(self):
        if self.due_date < timezone.now():
            raise ValidationError('Due date must be in the future.')

    def _validate_priority(self):
        if self.priority not in dict(self.PRIORITY_LEVELS).keys():
            raise ValidationError('Invalid priority level.')

    def _validate_status(self):
        if self.status not in dict(self.STATUS_CHOICES).keys():
            raise ValidationError('Invalid status value.')
    
    # Validations
    def clean(self):
        """
        Validate the model fields.
        """
        self._validate_due_date()
        self._validate_priority()
        self._validate_status()

    # Save Method
    def save(self, *args, **kwargs):
        """
        Override the save method to enforce validations and handle the completed_at timestamp.
        """
        
        self.full_clean() 

        if self.status == 'COMPLETED' and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status == 'PENDING':
            self.completed_at = None
            
        super(Task, self).save(*args, **kwargs)

    # String Representation
    def __str__(self):
        return self.title
    