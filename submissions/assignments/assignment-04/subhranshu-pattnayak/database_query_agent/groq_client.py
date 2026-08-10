'''
## Centralized Groq LLM client management.

This module exposes a default singleton Groq client for simple application-wide
LLM access while also providing a configurable GroqClient class for advanced
use cases requiring multiple models, custom settings, or isolated client
instances. The API is designed to offer a clean and consistent interface over
LangChain's ChatGroq implementation.

---
### Default Usage:

```
from groq_client import call_llm

response = call_llm("What is LangGraph?")
```

### Custom model usage:

```
from groq_client import set_model, call_llm

set_model("llama-3.3-70b-versatile")

response = call_llm("What is LangGraph?")
```

### Independent Client usage (multi-threaded use):

```
from groq_client import get_client

client_a = get_client(model="llama-3.3-70b-versatile")
client_b = get_client(model="openai/gpt-oss-120b")

response_a = client_a.call_llm("Hello")
response_b = client_b.call_llm("Hello")
```
'''


from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


class GroqClient:
    """
    Wrapper around ChatGroq that supports model configuration,
    runtime model switching, and LLM invocation.

    Can be used directly to create independent client instances,
    or through the module-level convenience functions which use
    a shared singleton client.
    """

    DEFAULT_MODEL = "openai/gpt-oss-120b"

    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0,
        **kwargs
    ):
        """
        Initialize a Groq client.

        Args:
            model: Model name to use. Falls back to DEFAULT_MODEL.
            temperature: Sampling temperature.
            **kwargs: Additional arguments passed to ChatGroq.
        """
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.kwargs = kwargs
        self._create_llm()
    
    def __getattr__(self, name):
        return getattr(self.llm, name)

    def _create_llm(self):
        """
        Create or recreate the underlying ChatGroq instance.
        """
        self.llm = ChatGroq(
            model=self.model,
            temperature=self.temperature,
            **self.kwargs
        )

    def set_model(self, model: str):
        """
        Change the active model and recreate the underlying client.

        Args:
            model: Name of the model to use.
        """
        if not model:
            raise ValueError("model must be a non-empty string")

        self.model = model
        self._create_llm()

    def get_model(self) -> str:
        """
        Return the currently configured model name.
        """
        return self.model

    def call_llm(self, messages):
        """
        Invoke the configured model with the provided messages.

        Args:
            messages: Input accepted by ChatGroq.invoke().

        Returns:
            The response returned by the model.
        """
        return self.llm.invoke(messages)


# Default singleton instance
_default_client = GroqClient()


# Convenience exports
def set_model(model: str):
    """
    Change the model used by the default singleton client.

    Args:
        model: Name of the model to use.
    """
    _default_client.set_model(model)


def get_model() -> str:
    """
    Return the model currently used by the default singleton client.
    """
    return _default_client.get_model()


def call_llm(messages):
    """
    Invoke the default singleton client.

    Args:
        messages: Input accepted by ChatGroq.invoke().

    Returns:
        The response returned by the model.
    """
    return _default_client.call_llm(messages)


def get_client(
    model: str | None = None,
    temperature: float = 0,
    **kwargs
):
    """
    Create an independent GroqClient instance.

    Args:
        model: Model name to use.
        temperature: Sampling temperature.

    Returns:
        A new GroqClient instance.
    """
    return GroqClient(
        model=model,
        temperature=temperature,
    )


__all__ = [
    "GroqClient",
    "call_llm",
    "set_model",
    "get_model",
    "get_client",
]