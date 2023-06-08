from django.db import models

class ChatUser(models.Model):
    username = models.CharField(max_length=150)
    anonymous = models.BooleanField()
    connected_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        if self.anonymous:
            return "??? %s connected at %s" % (self.username, self.connected_time)
        else:
            return "%s connected at %s" % (self.username, self.connected_time)