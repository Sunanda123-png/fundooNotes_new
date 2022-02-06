import logging

logging.basicConfig(filename="middleware.log", level=logging.INFO, filemode="w")
logger = logging.getLogger()


class CountRequestsMiddleware:
    """
    this middleware is created for counting the request
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.count_requests = 0

    def __call__(self, request, *args, **kwargs):
        self.count_requests += 1
        logger.info("{self.count_requests}")
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        print({view_func.__name__})
        pass

