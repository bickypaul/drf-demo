from django.db.models import Q
from rest_framework import generics, mixins
from postings.models import BlogPost
from .serializers import BlogPostSerializer
from .permissions import IsOwnerOrReadOnly


'''
API views from the generics class
'''
class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView): #DetailView
    lookup_field        ='pk'
    serializer_class    = BlogPostSerializer
    #queryset        = BlogPost.objects.all()

    def get_queryset(self):
        qs = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)
                ).distinct()
        return qs
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView): #DetailView
    lookup_field        ='pk'
    serializer_class    = BlogPostSerializer
    permission_classes  = [IsOwnerOrReadOnly]
    #queryset        = BlogPost.objects.all()

    def get_queryset(self):
        return BlogPost.objects.all()
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # since it is retrieve view we can also overide the get object method
    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return BlogPost.objects.get(pk=pk)
