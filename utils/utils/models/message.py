from dataclasses import dataclass, asdict
import uuid
from datetime import datetime

@dataclass
class ChatMessage:
    type: str
    sender: str
    text: str
    id: str = None
    timestamp: str = None

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return asdict(self)
