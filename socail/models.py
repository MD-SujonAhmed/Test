from django.db import models

class MessengerMessage(models.Model):
    sender_id = models.CharField(max_length=255)    
    message_text = models.TextField()               
    timestamp = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return f"{self.sender_id} - {self.timestamp}"