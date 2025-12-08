from typing import List, Dict, Any

class ConversationMemory:
    """
    A simple in-memory storage for conversation history.
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str):
        """Adds a message to the history."""
        self.history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, Any]]:
        """Returns the full conversation history."""
        return self.history

    def clear(self):
        """Clears the history."""
        self.history = []

    def get_context_string(self) -> str:
        """Returns the history formatted as a string for context."""
        context = ""
        for msg in self.history:
            context += f"{msg['role'].upper()}: {msg['content']}\n"
        return context
