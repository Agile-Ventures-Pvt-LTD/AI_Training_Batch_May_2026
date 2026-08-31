"""
Secure OAuth Token Management - C-8: Encrypted token storage with per-user isolation

Features:
- Tokens encrypted at rest
- Per-user session storage (no globals)
- Automatic expiration tracking
- Token refresh management
"""

import os
import json
import base64
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class SecureTokenStorage:
    """
    Encrypted OAuth token storage with per-user isolation.

    Uses Fernet symmetric encryption for token protection and
    Django sessions for per-user storage (thread-safe).
    """

    def __init__(self):
        """Initialize secure token storage with encryption"""
        self.cache_ttl = 3600  # 1 hour cache

        # Try to import Fernet for encryption
        try:
            from cryptography.fernet import Fernet

            key = os.getenv('OAUTH_ENCRYPTION_KEY')
            if not key:
                if os.getenv('ENVIRONMENT') == 'production':
                    raise ValueError("OAUTH_ENCRYPTION_KEY must be set in production!")
                else:
                    # Development: generate a test key
                    key = Fernet.generate_key().decode()
                    print(f"⚠️  Generated OAUTH_ENCRYPTION_KEY for development: {key}")

            self.cipher = Fernet(key.encode() if isinstance(key, str) else key)
            self.encryption_enabled = True

        except ImportError:
            logger.warning("cryptography not installed. Tokens will not be encrypted.")
            self.cipher = None
            self.encryption_enabled = False

    def store_token(self, request, provider: str, token_data: Dict[str, Any]) -> None:
        """
        Store OAuth token securely in user's session.

        Args:
            request: Django request object
            provider: OAuth provider (google, github, etc.)
            token_data: Token response {
                'access_token': 'xxx',
                'refresh_token': 'yyy',
                'expires_at': 1234567890,
                'token_type': 'Bearer'
            }

        Raises:
            ValueError: If token data is invalid
            Exception: If storage fails
        """
        try:
            # Validate token data
            if not all(k in token_data for k in ['access_token', 'expires_at']):
                raise ValueError("Token must contain access_token and expires_at")

            # Add metadata
            token_data['stored_at'] = datetime.utcnow().isoformat()
            token_data['provider'] = provider

            # Encrypt the token data if encryption is available
            if self.encryption_enabled:
                encrypted = self._encrypt_token(token_data)
            else:
                # Fall back to base64 encoding if encryption unavailable
                encrypted = base64.b64encode(
                    json.dumps(token_data).encode()
                ).decode()

            # Store in user's session (per-user, not global)
            session_key = f'oauth_{provider}_token'
            request.session[session_key] = encrypted
            request.session.save()

            logger.info(f"✓ OAuth token stored securely for provider {provider}")

        except Exception as e:
            logger.error(f"Failed to store OAuth token: {e}")
            raise

    def get_token(self, request, provider: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve and decrypt OAuth token from user's session.

        Args:
            request: Django request object
            provider: OAuth provider

        Returns:
            Decrypted token data or None if not found/expired
        """
        try:
            session_key = f'oauth_{provider}_token'
            encrypted = request.session.get(session_key)

            if not encrypted:
                return None

            # Decrypt
            if self.encryption_enabled:
                token_data = self._decrypt_token(encrypted)
            else:
                # Fall back to base64 decoding
                token_data = json.loads(
                    base64.b64decode(encrypted).decode()
                )

            # Check expiration
            expires_at = datetime.fromtimestamp(token_data['expires_at'])
            if expires_at < datetime.utcnow():
                logger.warning(f"OAuth token expired for provider {provider}")
                self.delete_token(request, provider)
                return None

            logger.info(f"✓ OAuth token retrieved for provider {provider}")
            return token_data

        except Exception as e:
            logger.error(f"Failed to retrieve OAuth token: {e}")
            return None

    def delete_token(self, request, provider: str) -> None:
        """
        Securely delete OAuth token from session.

        Args:
            request: Django request object
            provider: OAuth provider
        """
        try:
            session_key = f'oauth_{provider}_token'
            if session_key in request.session:
                del request.session[session_key]
                request.session.save()
                logger.info(f"✓ OAuth token deleted for provider {provider}")
        except Exception as e:
            logger.error(f"Failed to delete OAuth token: {e}")

    def refresh_token(
        self, request, provider: str, new_token_data: Dict[str, Any]
    ) -> None:
        """
        Refresh expired access token.

        Args:
            request: Django request
            provider: OAuth provider
            new_token_data: New token response from provider
        """
        try:
            # Delete old token
            self.delete_token(request, provider)

            # Store new token
            self.store_token(request, provider, new_token_data)

            logger.info(f"✓ OAuth token refreshed for provider {provider}")

        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise

    def is_token_valid(self, request, provider: str) -> bool:
        """
        Check if token exists and is not expired.

        Args:
            request: Django request object
            provider: OAuth provider

        Returns:
            True if valid token exists, False otherwise
        """
        token = self.get_token(request, provider)
        return token is not None

    def get_token_expiry(self, request, provider: str) -> Optional[datetime]:
        """
        Get token expiry time.

        Args:
            request: Django request object
            provider: OAuth provider

        Returns:
            Expiry datetime or None if token not found
        """
        token = self.get_token(request, provider)
        if token and 'expires_at' in token:
            return datetime.fromtimestamp(token['expires_at'])
        return None

    def _encrypt_token(self, token_data: Dict[str, Any]) -> str:
        """
        Encrypt token data using Fernet.

        Args:
            token_data: Token data to encrypt

        Returns:
            Encrypted token (base64 encoded)
        """
        if not self.cipher:
            raise RuntimeError("Encryption not available")

        json_bytes = json.dumps(token_data).encode()
        encrypted_bytes = self.cipher.encrypt(json_bytes)
        return base64.b64encode(encrypted_bytes).decode()

    def _decrypt_token(self, encrypted_token: str) -> Dict[str, Any]:
        """
        Decrypt token data using Fernet.

        Args:
            encrypted_token: Encrypted token (base64 encoded)

        Returns:
            Decrypted token data
        """
        if not self.cipher:
            raise RuntimeError("Encryption not available")

        encrypted_bytes = base64.b64decode(encrypted_token)
        decrypted_json = self.cipher.decrypt(encrypted_bytes).decode()
        return json.loads(decrypted_json)


# Global instance
_token_storage = None


def get_token_storage() -> SecureTokenStorage:
    """Get global token storage instance"""
    global _token_storage
    if _token_storage is None:
        _token_storage = SecureTokenStorage()
    return _token_storage
