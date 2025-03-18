from .mixins.VideoEditorApp import VideoEditorAppMixin

class Client(VideoEditorAppMixin):
    def __init__(self):
        super().__init__()
        # Any additional initialization for Client
