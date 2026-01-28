from __future__ import annotations

from .mixins.VideoEditorApp import VideoEditorAppMixin

class Client(VideoEditorAppMixin):
    def __init__(self) -> None:
        super().__init__()
        # Any additional initialization for Client
