"""
設定管理モジュール

YAMLファイルと環境変数から設定を読み込み、アプリケーション全体で使用する設定を管理します。
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
import logging.config


class Config:
    """アプリケーション設定を管理するクラス"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        設定を初期化します。
        
        Args:
            config_path: 設定ファイルのパス（デフォルトは config/config.yaml）
        """
        self.config_path = config_path or Path("config/config.yaml")
        self._config: Dict[str, Any] = {}
        self._load_config()
        self._load_environment_variables()
        self._setup_logging()
    
    def _load_config(self) -> None:
        """YAMLファイルから設定を読み込みます。"""
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}
        else:
            raise FileNotFoundError(f"設定ファイルが見つかりません: {self.config_path}")
    
    def _load_environment_variables(self) -> None:
        """環境変数から設定を上書きします。"""
        # Google Sheets設定
        if google_creds := os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            self._config.setdefault("export", {}).setdefault("google_sheets", {})["credentials_path"] = google_creds
        
        if spreadsheet_id := os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID"):
            self._config.setdefault("export", {}).setdefault("google_sheets", {})["spreadsheet_id"] = spreadsheet_id
        
        # スクレイピング設定
        if base_url := os.getenv("SCRAPING_BASE_URL"):
            self._config.setdefault("scraping", {})["base_url"] = base_url
        
        # ログレベル
        if log_level := os.getenv("LOG_LEVEL"):
            self._config.setdefault("logging", {})["level"] = log_level
        
        # データベース設定
        if db_path := os.getenv("DATABASE_PATH"):
            self._config.setdefault("database", {}).setdefault("sqlite", {})["path"] = db_path
        
        # 並行処理設定
        if max_workers := os.getenv("MAX_WORKERS"):
            self._config.setdefault("scraping", {}).setdefault("concurrency", {})["max_workers"] = int(max_workers)
        
        if rate_limit := os.getenv("RATE_LIMIT_SECONDS"):
            self._config.setdefault("scraping", {}).setdefault("concurrency", {})["rate_limit"] = float(rate_limit)
        
        # デバッグ設定
        if debug := os.getenv("DEBUG"):
            self._config.setdefault("app", {}).setdefault("debug", {})["verbose"] = debug.lower() == "true"
        
        # キャッシュ設定
        if cache_enabled := os.getenv("CACHE_ENABLED"):
            self._config.setdefault("app", {}).setdefault("cache", {})["enabled"] = cache_enabled.lower() == "true"
        
        if cache_ttl := os.getenv("CACHE_TTL"):
            self._config.setdefault("app", {}).setdefault("cache", {})["ttl"] = int(cache_ttl)
    
    def _setup_logging(self) -> None:
        """ロギング設定をセットアップします。"""
        logging_config_path = Path("config/logging.yaml")
        if logging_config_path.exists():
            with open(logging_config_path, "r", encoding="utf-8") as f:
                logging_config = yaml.safe_load(f)
                
                # ログディレクトリを作成
                log_dir = Path("logs")
                log_dir.mkdir(exist_ok=True)
                
                logging.config.dictConfig(logging_config)
        else:
            # デフォルトのロギング設定
            logging.basicConfig(
                level=self.get("logging.level", "INFO"),
                format=self.get("logging.format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        ドット記法で設定値を取得します。
        
        Args:
            key: 設定キー（例: "scraping.base_url"）
            default: デフォルト値
            
        Returns:
            設定値またはデフォルト値
        """
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """すべての設定を取得します。"""
        return self._config.copy()
    
    @property
    def scraping_config(self) -> Dict[str, Any]:
        """スクレイピング設定を取得します。"""
        return self.get("scraping", {})
    
    @property
    def database_config(self) -> Dict[str, Any]:
        """データベース設定を取得します。"""
        return self.get("database", {})
    
    @property
    def export_config(self) -> Dict[str, Any]:
        """エクスポート設定を取得します。"""
        return self.get("export", {})
    
    @property
    def app_config(self) -> Dict[str, Any]:
        """アプリケーション設定を取得します。"""
        return self.get("app", {})


# シングルトンインスタンス
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """設定インスタンスを取得します。"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance 