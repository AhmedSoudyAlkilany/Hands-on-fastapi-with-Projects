from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid

@dataclass
class Message:

    role : str
    content : str
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Conversation:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_message(self, role:str, content:str)-> Message:
        msg = Message(role=role, content=content)
        self.messages.append(msg)
        self.updated_at = datetime.utcnow()
        return msg
    
    def add_exchange(self, user_msg: str, assistant_msg: str):
        
        self.add_message("user", user_msg)
        self.add_message("assistant", assistant_msg)

    def get_history(self, max_messages: int = 10) -> List[Message]:
        
        return self.messages[-max_messages:]

    @property
    def message_count(self) -> int:
        return len(self.messages)

    def auto_title(self) -> str:
        
        for msg in self.messages:
            if msg.role == "user":
                title = msg.content[:50]
                if len(msg.content) > 50:
                    title += "..."
                self.title = title
                return title
        return "New Conversation"   