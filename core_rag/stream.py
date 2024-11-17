from typing import Optional
from langchain_core.messages import BaseMessage


async def astream_state(
    app,
    res,
    history
    # input
):
    """Stream messages from the runnable."""
    root_run_id: Optional[str] = None
    messages: dict[str, BaseMessage] = {}

    async for event in app.astream_events(
        {"question": res['question'], "context": res['documents'], "history": history}, version="v1"
    ):
        if event["event"] == "on_chat_model_stream":
            message: BaseMessage = event["data"]["chunk"]
            yield message