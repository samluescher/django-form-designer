class HttpRedirectException(Exception):
    def __init__(self, url, *args, **kwargs):
        self.url = url
        super(HttpRedirectException, self).__init__(*args, **kwargs)
