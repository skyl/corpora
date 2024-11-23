import os

from django.http import HttpResponse
from django.views import View


class BinaryView(View):
    def get(self, request, arch, *args, **kwargs):
        path = f"/workspace/rs/target/{arch}/release/corpora"
        if not os.path.exists(path):
            return HttpResponse("Binary not found", status=404)

        with open(path, "rb") as binary_file:
            response = HttpResponse(
                binary_file.read(), content_type="application/octet-stream",
            )
            response["Content-Disposition"] = "attachment; filename=corpora"
            return response
