from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .helpers import Exporter


@login_required
def export(request):
    """Exports instances as a json file."""
    exporter = Exporter()
    data = exporter.data
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="export.json"'
    return response