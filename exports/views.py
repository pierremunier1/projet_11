from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .helpers import Exporter


@login_required
def export(request):
    """Exports instances as a json file."""
    exporter = Exporter()
    return JsonResponse(exporter.data, safe=False)
