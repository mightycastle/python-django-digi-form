from django.http import HttpResponse
from django.views.generic import View
import json

from emails.apis import render_html_email


class EmailTestingView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        try:
            context_json = self.kwargs['context_json']
            if context_json:
                extra_context = json.loads(context_json)
                context.update(extra_context)
        except StandardError:
            pass

        result_str = render_html_email(self.kwargs['file_name'], context)
        return HttpResponse(result_str)
