from django.utils import timezone

class VisitLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # سجل بسيط في الـ console (للمشروع/التطوير)
        try:
            ip = request.META.get("REMOTE_ADDR")
            print(f"[{timezone.now()}] {request.method} {request.path} - {ip}")
        except Exception:
            pass

        return response
