from django.db import models
from django.conf import settings
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse

# Django Hosts ---> that handles subdomain for reverse

class BlogPost(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=120, null=True, blank=True)
    content     = models.TextField(max_length=120, null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title #self.user.username can also be used here.

    @property
    def owner(self):
        return self.user

    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk}) /api/postings/1
    
    def get_api_url(self, request=None):
        return api_reverse('api-postings:post-rud', kwargs={'pk':self.pk}, request=request)


# when the full url was not showing up in the json output, 
# it was the context issue, to fix that in the method get_api_url
# we had to request argument as None initially.