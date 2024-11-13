import subprocess

from django.http import HttpResponse
from django.views import View


class BuildBinaryView(View):
    def get(self, request, *args, **kwargs):
        try:
            # root_dir = "/workspace"
            # cli_main = "/workspace/py/packages/corpora_cli/main.py"
            output_path = "/workspace/dist/corpora_static"

            # subprocess.run(
            #     ["pyinstaller", "--onefile", cli_main, "--name", "corpora"],
            #     check=True,
            #     cwd=root_dir,
            # )

            with open(output_path, "rb") as binary_file:
                response = HttpResponse(
                    binary_file.read(), content_type="application/octet-stream"
                )
                response["Content-Disposition"] = "attachment; filename=corpora"
                return response

        except Exception as e:
            # Handle exceptions if PyInstaller fails
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
