from ninja import Router

from .auth import BearerAuth
from .routers.corpus import corpus_router
from .routers.corpustextfile import file_router
from .routers.split import split_router
from .routers.plan import plan_router
from .routers.workon import workon_router


api = Router(tags=["corpora"], auth=BearerAuth())

api.add_router("corpus", corpus_router)
api.add_router("file", file_router)
api.add_router("split", split_router)
api.add_router("plan", plan_router)
api.add_router("workon", workon_router)
