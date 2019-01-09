from rest_framework import serializers
from postings.models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer): #forms.ModelForm
    url                = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BlogPost
        fields = [
            'url',
            'pk',
            'user',
            'title',
            'content',
            'timestamp'
        ]
        read_only_fields = ['id','user']

    def get_url(self, obj):
        # to get the request here, we need a method in RUD view.
        # the method name would be get_serializer_context(self, *args, **kwargs)
        request = self.context.get("request")
        return obj.get_api_url(request=request)


    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value) #inlcuding instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title has already been used.")
        return value        

    # converts to JSON
    # Validations for data passed