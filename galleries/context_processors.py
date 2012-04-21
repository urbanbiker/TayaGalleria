from django.conf import settings

def development_settings(request):
    context_extras = dict(
        TEMPLATE_DEBUG=settings.TEMPLATE_DEBUG)
    return context_extras
