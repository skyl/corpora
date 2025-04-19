import base64
import os
from typing import Dict

import aiofiles
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from corpora_ai.llm_interface import ChatCompletionTextMessage
from corpora_ai.provider_loader import load_llm_provider
from ninja import Router, Schema
from ninja.errors import HttpError

from corpora.auth import BearerAuth
from corpora.schema.chat import CorpusChatSchema, get_additional_context

PYTHON_PLOT_SYSTEM_MESSAGE = (
    "You are a skilled assistant focused on creating clear, actionable Python code for plotting. "
    "Given the user input, generate a concise Python code snippet that: "
    "- Uses np for NumPy, plt for Matplotlib, and sp for SymPy (already imported). "
    "- Creates a high-quality plot (e.g., 2D line, 3D surface, histogram) with labels, title, and grid. "
    "- Saves the plot to 'plot.png' using plt.savefig('plot.png'). "
    "- Closes the figure with plt.close() to avoid memory leaks. "
    "- Does NOT include import statements. "
    "Return only the Python code as a string, no explanations."
)


class PythonCodeSchema(Schema):
    code: str


class PlotResponseSchema(Schema):
    plot: str


plots_router = Router(tags=["plots"], auth=BearerAuth())


@plots_router.post(
    "/matplotlib",
    response=PlotResponseSchema,
    operation_id="get_matplotlib_plot",
)
async def get_matplotlib_plot(
    request,
    payload: CorpusChatSchema,
) -> Dict[str, str]:
    messages = [
        ChatCompletionTextMessage(
            role="system",
            text=f"{PYTHON_PLOT_SYSTEM_MESSAGE}{get_additional_context(payload)}",
        ),
        *[
            ChatCompletionTextMessage(role=msg.role, text=msg.text)
            for msg in payload.messages
        ],
    ]

    llm = load_llm_provider()
    pycode = llm.get_data_completion(messages, PythonCodeSchema).code

    plot_path = "plot.png"
    exec(pycode, {"np": np, "plt": plt, "sp": sp})

    if not os.path.exists(plot_path):
        raise HttpError(400, "No plot generated")

    async with aiofiles.open(plot_path, "rb") as f:
        png_bytes = await f.read()

    os.remove(plot_path)
    png_base64 = base64.b64encode(png_bytes).decode("utf-8")
    return {"plot": png_base64}
