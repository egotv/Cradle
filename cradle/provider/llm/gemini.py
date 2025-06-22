import os
import asyncio
from typing import Any, Dict, List, Tuple, Optional

import backoff

try:
    # google-generativeai is required. If it is missing, we'll raise a helpful error later.
    import google.generativeai as genai
except ImportError as e:  # pragma: no cover
    genai = None

# Provide a fallback for static type checkers if stubs are missing
if genai is not None and not hasattr(genai, "GenerationConfig"):
    from typing import Any as _Any

    class _DummyGenerationConfig:  # noqa: D401
        def __init__(self, *args: _Any, **kwargs: _Any) -> None:
            pass

    genai.GenerationConfig = _DummyGenerationConfig  # type: ignore[attr-defined]

from cradle.provider.llm.restful_claude import RestfulClaudeProvider
from cradle.config import Config
from cradle.log import Logger
from cradle.utils.json_utils import load_json
from cradle.utils.file_utils import assemble_project_path

config = Config()
logger = Logger()

# These are keys used **inside** the JSON config file. Do not change them.
PROVIDER_SETTING_KEY_VAR = "key_var"      # Environment variable name holding Google API key
PROVIDER_SETTING_COMP_MODEL = "comp_model" # Gemini model name (e.g. gemini-1.5-pro, gemini-2.5-pro, etc.)


class GeminiProvider(RestfulClaudeProvider):
    """LLM provider that calls Google Gemini models via the official `google-generativeai` SDK.

    NOTE: This class only handles completion-style requests. For embeddings we still fall back to
    OpenAI (handled by `LLMFactory`).
    """

    client: Any = None  # ``google.generativeai.GenerativeModel`` instance
    llm_model: str = ""

    def __init__(self) -> None:  # noqa: D401
        super().__init__()
        self.retries = 5  # Same retry policy as the other providers

    # ---------------------------------------------------------------------
    # Provider initialisation
    # ---------------------------------------------------------------------
    def init_provider(self, provider_cfg) -> None:  # type: ignore[override]
        """Initialise with a path or dict containing the provider config."""
        self.provider_cfg = self._parse_config(provider_cfg)

    def _parse_config(self, provider_cfg) -> Dict[str, Any]:  # noqa: C901
        if isinstance(provider_cfg, dict):
            conf_dict = provider_cfg
        else:
            path = assemble_project_path(provider_cfg)
            conf_dict = load_json(path)

        if genai is None:
            raise ImportError(
                "The `google-generativeai` package is required for the Gemini provider.\n"
                "Install it with `pip install google-generativeai`."
            )

        # Read API key from env and configure the client.
        key_var_name = conf_dict[PROVIDER_SETTING_KEY_VAR]
        api_key = os.getenv(key_var_name)
        if api_key is None or api_key == "":
            raise EnvironmentError(
                f"Environment variable '{key_var_name}' is not set. Please export your Google "
                f"Gemini API key before running."
            )

        genai.configure(api_key=api_key)  # type: ignore[attr-defined]

        # Model name (e.g. 'gemini-1.5-pro-latest' or 'gemini-2.5-pro').
        self.llm_model = conf_dict[PROVIDER_SETTING_COMP_MODEL]

        # Initialise model handle (this is lightweight – it does not make a network call).
        self.client = genai.GenerativeModel(self.llm_model)  # type: ignore[attr-defined]

        return conf_dict

    # ---------------------------------------------------------------------
    # Completion helpers
    # ---------------------------------------------------------------------
    @staticmethod
    def _messages_to_prompt(messages: List[Dict[str, Any]]) -> str:
        """Convert OpenAI-style chat *messages* into a single prompt string suitable for Gemini.

        At the moment we do a very simple conversion that concatenates the text portions of each
        message, prefixed with the role name. Non-text parts (e.g. images) are ignored. This keeps
        the implementation straightforward while still preserving most of the conversation
        context. If you rely on multi-modal prompting, you will need to extend this to use the
        SDK's structured parts API.
        """
        prompt_lines: List[str] = []
        for msg in messages:
            role = msg.get("role", "user")
            content_field = msg.get("content", "")

            # The framework constructs **content** as a list of dicts when supporting images.
            # We'll extract just the text portions.
            if isinstance(content_field, list):
                texts = [part.get("text", "") for part in content_field if part.get("type") == "text"]
                content = "\n".join(texts)
            else:
                # For backward compatibility if content is a simple string.
                content = str(content_field)

            prompt_lines.append(f"{role.capitalize()}: {content}")

        return "\n".join(prompt_lines)

    def create_completion(  # type: ignore[override]
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = config.temperature,
        seed: Optional[int] = config.seed,  # Unused for Gemini currently, kept for API compatibility
        max_tokens: int = config.max_tokens,
    ) -> Tuple[str, Dict[str, int]]:

        if model is None:
            model = self.llm_model

        # Pretty-print the prompt that will be sent to Gemini
        # import json, textwrap
        # print("\n===== GEMINI PROMPT =====")
        # print(textwrap.indent(json.dumps(messages, ensure_ascii=False, indent=2), "  "))
        # print("=========================\n")

        if config.debug_mode:
            logger.debug(
                f"Creating Gemini completion with model {model}, temperature {temperature}, "
                f"max_tokens {max_tokens}"
            )
        else:
            logger.write(f"Requesting {model} completion via Gemini API…")

        @backoff.on_exception(
            backoff.constant,
            (Exception,),  # Retry on any exception from the SDK/network
            max_tries=self.retries,
            interval=10,
        )
        def _generate_response_with_retry(prompt: str):
            response = self.client.generate_content(
            prompt_text,
            generation_config = genai.GenerationConfig(
                temperature      = temperature,
                max_output_tokens= max_tokens,
            ),
            safety_settings=[    # each needs both keys
                { "category": "HARM_CATEGORY_DANGEROUS",   "threshold": "BLOCK_NONE" },
                { "category": "HARM_CATEGORY_HARASSMENT",  "threshold": "BLOCK_NONE" },
                { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE" },
                { "category": "HARM_CATEGORY_SEXUAL",      "threshold": "BLOCK_NONE" },
            ],
        )
            if response is None:
                raise RuntimeError("Received empty response from Gemini API.")
            return response

        prompt_text = self._messages_to_prompt(messages)
        response = _generate_response_with_retry(prompt_text)

        # Extract the generated text
        message_text = response.text if hasattr(response, "text") else str(response)

        # Usage information is optional (depends on API account type)
        usage = getattr(response, "usage_metadata", {}) or {}
        info = {
            "prompt_tokens": usage.get("prompt_token_count", 0),
            "completion_tokens": usage.get("candidates_token_count", 0),
            "total_tokens": usage.get("total_token_count", 0),
        }

        logger.write(f"Response received from {model}.")
        return message_text, info

    async def create_completion_async(  # type: ignore[override]
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = config.temperature,
        seed: Optional[int] = config.seed,  # Unused
        max_tokens: int = config.max_tokens,
    ) -> Tuple[str, Dict[str, int]]:
        # Off-load the sync implementation to a thread so we don't block the event loop.
        return await asyncio.to_thread(
            self.create_completion,
            messages,
            model,
            temperature,
            seed,
            max_tokens,
        )

    # ------------------------------------------------------------------
    # Token helper – optional, but keeps the interface consistent.
    # ------------------------------------------------------------------
    def num_tokens_from_messages(self, messages, model):  # noqa: D401, N802
        """A very rough token count implementation for budgeting.

        Gemini counts tokens differently from OpenAI's models and, at the time of writing, the SDK
        does not expose a dedicated tokenizer. We'll approximate by counting *words*; this is by no
        means perfect but gives a ball-park figure that is good enough for basic budgeting.
        """
        prompt = self._messages_to_prompt(messages)
        # Split on whitespace as a naive proxy.
        return len(prompt.split())

    # ------------------------------------------------------------------
    # Prompt assembly – reuse the existing Claude implementation (identical structure).
    # ------------------------------------------------------------------
    def assemble_prompt(self, template_str: str = None, params: Dict[str, Any] = None):  # type: ignore[override]
        # We inherit from RestfulClaudeProvider solely to reuse its elaborate prompt assembly logic.
        return super().assemble_prompt(template_str=template_str, params=params) 