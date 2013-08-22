from form_designer.exceptions import HttpRedirectException
from django.template.base import TemplateSyntaxError
from django.http import HttpResponseRedirect

class RedirectMiddleware(object):
    def process_exception(self, request, exception):
        #django wraps the original exception in a template exception if it
        #is raised in a node
        if isinstance(exception, TemplateSyntaxError):
            try:
                exception = exception.exc_info[1]
            except IndexError, e:
                return

        if isinstance(exception, HttpRedirectException):
            url = exception.url
            return HttpResponseRedirect(url)

