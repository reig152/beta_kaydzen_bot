from django.http import HttpResponse
from django.views import View
from aiohttp import web
from app.delivery.bot import __main__ as aiohttp_app

class TelegramWebhookView(View):
    def post(self, request, *args, **kwargs):
        # Forward the request to the aiohttp application
        aiohttp_request = web.Request(request)
        response = aiohttp_app.app._handle(aiohttp_request)
        return HttpResponse(status=response.status)