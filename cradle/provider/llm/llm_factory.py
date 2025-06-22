from cradle.provider.llm.openai import OpenAIProvider
from cradle.provider.llm.restful_claude import RestfulClaudeProvider
from cradle.provider.llm.gemini import GeminiProvider
from cradle.utils import Singleton
from cradle.provider.llm.hybrid import HybridProvider

class LLMFactory(metaclass=Singleton):

    def __init__(self):
        self._builders = {}


    def create(self, llm_provider_config_path, embed_provider_config_path, **kwargs):

        llm_provider = None
        embed_provider = None

        key = llm_provider_config_path

        if "openai" in key:
            llm_provider = OpenAIProvider()
            llm_provider.init_provider(llm_provider_config_path)
            embed_provider = llm_provider
        elif "claude" in key:
            llm_provider = RestfulClaudeProvider()
            llm_provider.init_provider(llm_provider_config_path)
            #logger.warn(f"Claude do not support embedding, use OpenAI instead.")
            embed_provider = OpenAIProvider()
            embed_provider.init_provider(embed_provider_config_path)
        elif "gemini" in key:
            llm_provider = GeminiProvider()
            llm_provider.init_provider(llm_provider_config_path)
            # Gemini currently has no embedding endpoint. Fall back to OpenAI for embeddings.
            embed_provider = OpenAIProvider()
            embed_provider.init_provider(embed_provider_config_path)
        elif "hybrid" in key:          # e.g. "./conf/hybrid_config.json"
            # llm_provider_config_path is a string path, so load the JSON file first
            import json, os
            with open(os.path.abspath(llm_provider_config_path), "r", encoding="utf-8") as f:
                hybrid_cfg = json.load(f)          # => {"gemini_cfg": "...", "openai_cfg": "..."}
            
            llm_provider = HybridProvider()
            llm_provider.init_provider(hybrid_cfg)   # pass the dict we just loaded
            embed_provider = OpenAIProvider()
            embed_provider.init_provider(embed_provider_config_path)

        if not llm_provider or not embed_provider:
            raise ValueError(key)

        return llm_provider, embed_provider
