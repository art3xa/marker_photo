from http import HTTPStatus
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json


class JSONResponseRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context['response'].exception:
            return json.dumps({
                'ok': False,
                'error': renderer_context['response'].data['detail'],
            })

        ok = renderer_context['response'].status_code <= 399
        if not ok:
            return json.dumps({
                'ok': False,
                'error': data if data is not None else HTTPStatus(renderer_context['response'].status_code).description,
            })

        return json.dumps({
            'ok': True,
            'data': data,
        })
