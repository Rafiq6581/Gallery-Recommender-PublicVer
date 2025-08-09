from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from zenml.client import Client
from zenml.exceptions import EntityExistsError


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # OpenAI API
    OPENAI_MODEL_ID: str = "gpt-4o-mini"
    OPENAI_API_KEY: str | None = None

    # Hugging Face API
    HUGGINGFACE_ACCESS_TOKEN: str | None = None

    # MongoDB
    DATABASE_HOST: str = "localhost"
    DATABASE_NAME: str = "gallery"
        
    # Comet
    COMET_API_KEY: str | None = None
    COMET_PROJECT: str = "gallery-recommender"

    # Google API Config
    SERVICE_ACCOUNT_FILE: str | None = None
    SCOPES: list[str] 
    GCP_PROJECT_ID: str = "artomo"
    GCP_REGION: str = "asia-northeast1"
    CLOUD_TASK_QUEUE: str = "gallery-report-queue"
    CLOUD_RUN_TASK_HANDLER_URL: str = "https://inference-api-525438826675.asia-northeast1.run.app"


    # Qdrant vector database
    USE_QDRANT_CLOUD: bool = False
    QDRANT_CLOUD_URL: str = ""
    QDRANT_APIKEY: str | None = None
    QDRANT_DATABASE_HOST: str = "localhost"
    QDRANT_DATABASE_PORT: int = 6333

    # AWS Authentication
    AWS_REGION: str = "ap-northeast-1"
    AWS_ACCESS_KEY: str | None = None
    AWS_SECRET_KEY: str | None = None
    AWS_ARN_ROLE: str | None = None

    # --- Optional settings used to tweak the code ---

    # AWS SageMaker
    HF_MODEL_ID: str = "meta-llama/Meta-Llama-3-8B-Instruct"
    GPU_INSTANCE: str = "ml.g5.2xlarge"
    SN_NUM_GPUS: int = 1 # number of GPUs per replica
    MAX_INPUT_LENGTH: int = 2048
    MAX_NUM_TOKENS: int = 4096
    MAX_BATCH_TOTAL_TOKENS: int = 4096 # max number of tokens in a batch
    COPIES: int = 1 # number of replicas
    GPUS: int = 1 # number of GPUs
    CPUS: int = 8 # number of CPU cores

    # OpenAI
    OPENAI_API_URL: str = "https://api.openai.com/v1/chat/completions"
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL_ID: str = "gpt-4o-mini"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 3000
    OPENAI_TOP_P: float = 0.9



    # RAG
    TEXT_EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    RERANKING_CROSS_ENCODER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-4-v2"
    RAG_MODEL_DEVICE: str = "cpu"


    @classmethod
    def load_settings(cls):
        """
        Tries to load the settings from the ZenML secret store.
        If that fails, it will take the settings from the .env file.

        Returns:
            Settings: The initialized settings object.
        """
        try:
            logger.info("Loading settings from ZenML secret store...")
            
            settings_secrets = Client().get_secret("settings")
            settings = cls(**settings_secrets.secret_values)
        
        except(RuntimeError, KeyError):
            logger.warning("Failed to load settings from ZenML secret store. Loading from .env file...")
            settings = cls()

        return settings
    
    def export(self) -> None:
        """
        Exports the settings to the ZenML secret store.
        """
        env_vars = settings.model_dump()
        for key, value in env_vars.items():
            env_vars[key] = str(value)

        client = Client()

        try:
            client.create_secret(
                name="settings",
                values=env_vars,
            )
        except EntityExistsError:
            logger.warning("Secret 'scope' already exists. Delete it manually by running 'zenml secret delete settings', before trying to recreate it.")
    

settings = Settings.load_settings()