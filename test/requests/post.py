import exceptions

class PostResponseDecider:
    def __init__(self):
        self.raise_http_error = False
        self.raise_exception = False
        self.stop_raise_exception_after = 0
        self.current_retry_number=0

    def reset(self):
        self.raise_http_error = False
        self.raise_exception = False
        self.stop_raise_exception_after = 0
        self.current_retry_number=0

    def set(self, raise_http_error=False, raise_exception=False, stop_raise_exception_after=0,
            current_retry_number=0):
        self.raise_http_error = raise_http_error
        self.raise_exception = raise_exception
        self.stop_raise_exception_after = stop_raise_exception_after
        self.current_retry_number=current_retry_number


class MockServer:
    def __init__(self):
        self.url = None
        self.data = []
        self.headers = None

    def reset(self):
        self.url = None
        self.data = []
        self.headers = None


class MockResponse:
    def __init__(self):
        self.status_code = None
        self.request = 'test_request'

    def reset(self):
        self.status_code = None

    def set(self, status_code):
        self.status_code = status_code

post_response_decider = PostResponseDecider()
mock_server = MockServer()
mock_response = MockResponse()


def post(url, data, headers):
    if post_response_decider.raise_http_error:
        exception = exceptions.HTTPError(exceptions.RequestException())
        exception.response = mock_response
        exception.message = 'Http error with error code %s ' % exception.response
        print 'exception type %s, content %s' % (type(exception), exception)
        raise exception
            #
            # exceptions.HTTPError(exceptions.RequestException(
            # response=mock_response.set(post_response_decider.status_code)), request=data)
    elif post_response_decider.raise_exception:
        pass
    else:
        mock_server.url = url
        mock_server.headers = headers
        mock_server.data.append(data)
        return mock_response