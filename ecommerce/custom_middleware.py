from django.utils.deprecation import MiddlewareMixin

class GoogleAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Example: Check if user is authenticated using Google
        if request.user.is_authenticated and request.user.socialaccount_set.filter(provider='google').exists():
            print(f"User {request.user} logged in using Google")
        return None
