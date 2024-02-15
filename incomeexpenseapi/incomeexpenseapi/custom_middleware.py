import datetime

class DateTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = datetime.datetime.now()
        response = self.get_response(request)
        response.end_time = datetime.datetime.now()
        return self.process_response(request, response)

    def process_response(self, request, response):
        response['X-Start-Time'] = str(request.start_time)
        response['X-End-Time'] = str(response.end_time)
        return response