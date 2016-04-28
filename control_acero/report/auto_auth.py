from django.contrib.auth.models import User

class Middleware(object):
    def process_request(self, request):
        request.user = User.objects.filter()[0]