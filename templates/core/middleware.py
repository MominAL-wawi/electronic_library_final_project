from django.utils import timezone

class VisitLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # تسجيل بسيط في console (مسموح للمشروع)
        if request.path.startswith('/'):
            print(f"[{timezone.now()}] {request.method} {request.path} - {request.META.get('REMOTE_ADDR')}")

        return response
