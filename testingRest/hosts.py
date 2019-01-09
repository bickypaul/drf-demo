from django.conf import settings
from django_hosts import patterns, host
from . import urls

host_patterns = patterns('', 
    host('api', urls, name='api'),
    host('postings', 'postings.urls', name='postings'),
)
