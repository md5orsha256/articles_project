from django.http import HttpResponse


class ExampleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Код, вызываемый перед представлением при каждом запросе.
        print("before_view")

        request_path_data = request.path.split("/")
        for path in request_path_data:
            try:
                id = int(path)
                if id < 100:
                    return HttpResponse("id от 1 до 100 зарезервированы")
            except ValueError:
                pass

        # return HttpResponse("vsdvsdsd")
        response = self.get_response(request)

        print("after_view")
        # Код, вызываемый после представления при каждом запросе.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print(view_func, view_args, view_kwargs)
    # Код, вызываемый непосредственно перед кодом представления.

    def process_exception(self, request, exception):
        pass
    # Код, вызываемый при выбросе исключения.

    def process_template_response(self, request, response):
        # Код, вызываемый при наличии в запросе метода render().
        # response["Content-Type"] = 'text/plain; charset=UTF-8'
        return response


class Example2Middleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Код, вызываемый перед представлением при каждом запросе.
        print("before_view2")

        # return HttpResponse("vsdvsdsd")
        response = self.get_response(request)

        print("after_view2")
        # Код, вызываемый после представления при каждом запросе.
        return response