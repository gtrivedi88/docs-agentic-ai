"""
Configuration management using Pydantic Settings.
Loads from .env file and environment variables.
"""
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Project Configuration
    project_name: str = Field(default="developerhub", description="Project name")
    project_key: str = Field(default="DEV", description="Jira project key")
    
    # LLM Configuration
    mistral_api_key: str = Field(..., description="Mistral API key")
    mistral_model: str = Field(default="mistral-large-latest", description="Mistral model name")
    temperature: float = Field(default=0.1, description="LLM temperature")
    max_tokens: int = Field(default=4096, description="Max tokens per response")
    
    # Jira Configuration
    jira_server: str = Field(..., description="Jira server URL")
    jira_user: str = Field(..., description="Jira username/email")
    jira_api_token: str = Field(..., description="Jira API token")
    
    # GitHub Configuration
    github_token: str = Field(..., description="GitHub personal access token")
    github_org: str = Field(..., description="GitHub organization")
    github_repos: str = Field(..., description="Comma-separated GitHub repos")
    
    # GitLab Configuration
    gitlab_url: Optional[str] = Field(default=None, description="GitLab URL")
    gitlab_token: Optional[str] = Field(default=None, description="GitLab token")
    gitlab_project_ids: Optional[str] = Field(default=None, description="GitLab project IDs")
    
    # Confluence Configuration
    confluence_url: str = Field(..., description="Confluence URL")
    confluence_user: str = Field(..., description="Confluence username")
    confluence_api_token: str = Field(..., description="Confluence API token")
    confluence_space: str = Field(..., description="Confluence space key")
    
    # Slack Configuration
    slack_bot_token: Optional[str] = Field(default=None, description="Slack bot token")
    slack_channels: Optional[str] = Field(default=None, description="Slack channels to monitor")
    
    # Google Docs Configuration
    google_credentials_file: Optional[str] = Field(default=None, description="Google credentials")
    
    # Vector Store Configuration
    chroma_persist_directory: str = Field(default="./data/vector_db")
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    
    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="./outputs/logs/lyra.log")
    
    # Agent Configuration
    max_iterations: int = Field(default=50, description="Max ReAct iterations")
    max_tool_calls: int = Field(default=100, description="Max tool calls per task")
    enable_cache: bool = Field(default=True, description="Enable API caching")
    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds")
    
    # Computed Properties
    @property
    def github_repo_list(self) -> List[str]:
        """Parse GitHub repos from comma-separated string."""
        return [repo.strip() for repo in self.github_repos.split(",")]
    
    @property
    def slack_channel_list(self) -> List[str]:
        """Parse Slack channels from comma-separated string."""
        if not self.slack_channels:
            return []
        return [ch.strip() for ch in self.slack_channels.split(",")]


# Global settings instance
settings = Settings()

