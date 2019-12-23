from django.views.generic import TemplateView


class Dashboard(TemplateView):
    """
    This is the dashboard app or main interface to interact with all other apps.
    Like a single page app.
    """

    template_name = 'frontend/base.html'
