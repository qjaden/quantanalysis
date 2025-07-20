"""Internationalization (i18n) support module

This module provides multi-language support following standard i18n practices.
Supports Chinese (zh) and English (en) by default.
"""

import os
import json
import warnings
from typing import Dict, Any, Optional
from pathlib import Path


class I18nManager:
    """Internationalization manager for multi-language support"""
    
    def __init__(self, default_language: str = "zh"):
        """Initialize i18n manager
        
        Args:
            default_language: Default language code ('zh' or 'en')
        """
        self.default_language = default_language
        self.current_language = default_language
        self.translations: Dict[str, Dict[str, str]] = {}
        self.supported_languages = ["zh", "en"]
        
        # Load translations
        self._load_translations()
    
    def _load_translations(self) -> None:
        """Load translation files from locales directory"""
        locales_dir = Path(__file__).parent / "locales"
        
        if not locales_dir.exists():
            warnings.warn(f"Locales directory not found: {locales_dir}")
            return
        
        for lang in self.supported_languages:
            lang_file = locales_dir / f"{lang}.json"
            if lang_file.exists():
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                except Exception as e:
                    warnings.warn(f"Failed to load translation file {lang_file}: {e}")
    
    def set_language(self, language: str) -> None:
        """Set current language
        
        Args:
            language: Language code ('zh' or 'en')
        """
        if language not in self.supported_languages:
            warnings.warn(f"Unsupported language: {language}. Using {self.default_language}")
            language = self.default_language
        
        self.current_language = language
    
    def t(self, key: str, **kwargs) -> str:
        """Translate a key to current language
        
        Args:
            key: Translation key (dot notation supported, e.g., 'metrics.total_return')
            **kwargs: Variables for string formatting
            
        Returns:
            Translated string
        """
        # Get translation for current language
        translation = self._get_translation(key, self.current_language)
        
        # If not found, try default language
        if translation is None and self.current_language != self.default_language:
            translation = self._get_translation(key, self.default_language)
        
        # If still not found, return the key itself
        if translation is None:
            translation = key
        
        # Format with provided variables
        try:
            return translation.format(**kwargs) if kwargs else translation
        except KeyError as e:
            warnings.warn(f"Missing variable in translation: {e}")
            return translation
    
    def _get_translation(self, key: str, language: str) -> Optional[str]:
        """Get translation for specific language
        
        Args:
            key: Translation key (supports dot notation)
            language: Language code
            
        Returns:
            Translation string or None if not found
        """
        if language not in self.translations:
            return None
        
        # Support dot notation (e.g., 'metrics.total_return')
        keys = key.split('.')
        translation = self.translations[language]
        
        try:
            for k in keys:
                translation = translation[k]
            return translation
        except (KeyError, TypeError):
            return None
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
    
    def get_supported_languages(self) -> list:
        """Get list of supported language codes"""
        return self.supported_languages.copy()
    
    def format_number(self, value: float, format_type: str = "percentage") -> str:
        """Format number according to current locale
        
        Args:
            value: Number to format
            format_type: 'percentage', 'decimal', 'currency'
            
        Returns:
            Formatted string
        """
        if format_type == "percentage":
            if self.current_language == "zh":
                return f"{value:.2%}"
            else:
                return f"{value:.2%}"
        elif format_type == "decimal":
            if self.current_language == "zh":
                return f"{value:.4f}"
            else:
                return f"{value:.4f}"
        else:
            return str(value)


# Global i18n instance
_i18n_manager = I18nManager()


def set_language(language: str) -> None:
    """Set global language"""
    _i18n_manager.set_language(language)


def get_language() -> str:
    """Get current global language"""
    return _i18n_manager.get_current_language()


def t(key: str, **kwargs) -> str:
    """Global translation function"""
    return _i18n_manager.t(key, **kwargs)


def format_number(value: float, format_type: str = "percentage") -> str:
    """Global number formatting function"""
    return _i18n_manager.format_number(value, format_type)


def get_supported_languages() -> list:
    """Get supported languages"""
    return _i18n_manager.get_supported_languages()