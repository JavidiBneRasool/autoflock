"""
config_loader.py
================
Universal credential loader for all agents.

BEFORE (insecure):
    with open('config/social.json') as f:
        config = json.load(f)
    token = config['telegram_bot_token']

AFTER (secure):
    from config_loader import get_credential
    token = get_credential('telegram_bot_token', flock='newshourflock')

All credentials are:
  - Loaded from encrypted vault at startup
  - Held in memory only
  - Never persisted to disk plaintext
  - Logged for audit trail
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# Import VaultFlock
import sys
sys.path.insert(0, str(Path.home() / 'projects/media/omni'))
from vault_agent import VaultFlock


class CredentialLoader:
    """
    Loads credentials from encrypted vault.
    In-memory cache to avoid repeated decryption.
    """
    
    def __init__(self):
        self.vault = VaultFlock()
        self._cache = {}
        self._audit_log = []
        self._load_vault()
    
    def _load_vault(self):
        """Load and cache all credentials at startup"""
        try:
            self._cache = self.vault.unlock_vault()
            self._log_access("LOAD", "vault_startup", "success")
        except Exception as e:
            self._log_access("LOAD", "vault_startup", f"error: {e}")
            raise
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get a credential by key.
        
        Args:
            key: Credential key (e.g., 'telegram_bot_token')
            default: Default value if not found
        
        Returns:
            Credential value or default
        """
        value = self._cache.get(key, default)
        
        if value is None:
            self._log_access("GET", key, "NOT_FOUND")
        else:
            # Log access but don't log the value
            self._log_access("GET", key, "success")
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all credentials as dict (in-memory only)"""
        self._log_access("GET_ALL", "all_credentials", f"count={len(self._cache)}")
        return self._cache.copy()
    
    def get_by_flock(self, flock: str) -> Dict[str, Any]:
        """
        Get all credentials for a specific flock.
        
        Args:
            flock: Flock name (e.g., 'newshourflock', 'marketflock')
        
        Returns:
            Dict of credentials for that flock
        """
        prefix = f"{flock}_"
        filtered = {
            k: v for k, v in self._cache.items()
            if k.startswith(prefix)
        }
        self._log_access("GET_BY_FLOCK", flock, f"found={len(filtered)}")
        return filtered
    
    def get_credential(self, key: str, flock: Optional[str] = None) -> Optional[str]:
        """
        Get a specific credential, optionally filtered by flock.
        
        Args:
            key: Credential key
            flock: Optional flock name prefix
        
        Returns:
            Credential value
        """
        if flock:
            full_key = f"{flock}_{key}"
            return self.get(full_key)
        else:
            return self.get(key)
    
    def _log_access(self, action: str, key: str, result: str):
        """Audit log for all credential access"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "key": key,
            "result": result
        }
        self._audit_log.append(entry)
    
    def get_audit_log(self) -> list:
        """Return audit trail of all credential access"""
        return self._audit_log.copy()
    
    def save_audit_log(self, filepath: Optional[str] = None):
        """
        Save audit log to file for security review.
        Default: ~/.omni_vault/audit.log
        """
        if filepath is None:
            filepath = Path.home() / ".omni_vault" / "audit.log"
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            for entry in self._audit_log:
                f.write(json.dumps(entry) + "\n")
        
        print(f"✅ Audit log saved: {filepath}")


# Global instance
_loader = None

def get_config() -> CredentialLoader:
    """Get global credential loader"""
    global _loader
    if _loader is None:
        _loader = CredentialLoader()
    return _loader


def get_credential(key: str, flock: Optional[str] = None) -> Optional[str]:
    """
    Shorthand: Get a single credential
    
    Example:
        token = get_credential('telegram_bot_token', flock='newshourflock')
    """
    return get_config().get_credential(key, flock)


def get_all_credentials() -> Dict[str, Any]:
    """Get all loaded credentials"""
    return get_config().get_all()


def get_flock_config(flock: str) -> Dict[str, Any]:
    """
    Get all credentials for a specific flock
    
    Example:
        config = get_flock_config('marketflock')
    """
    return get_config().get_by_flock(flock)


# Backward compatibility wrapper
class ConfigLoader:
    """
    Drop-in replacement for old load_config() function.
    Can be used as: config = ConfigLoader().load(flock='newshourflock')
    """
    
    def __init__(self):
        self.loader = get_config()
    
    def load(self, flock: Optional[str] = None) -> Dict[str, Any]:
        """Load config for a flock"""
        if flock:
            return self.get_flock_config(flock)
        else:
            return self.get_all_credentials()
    
    def get_flock_config(self, flock: str) -> Dict[str, Any]:
        """Load config for specific flock"""
        return self.loader.get_by_flock(flock)


# Example usage
if __name__ == "__main__":
    print("🔑 Credential Loader Test\n")
    
    # Load and display
    config = get_config()
    all_creds = config.get_all()
    
    print(f"✅ Loaded {len(all_creds)} credentials from vault")
    print(f"\nAvailable keys:")
    for key in all_creds.keys():
        print(f"  - {key}")
    
    print(f"\nAudit trail:")
    for entry in config.get_audit_log():
        print(f"  {entry['timestamp']} | {entry['action']:10} | {entry['key']:40} | {entry['result']}")
    
    print("\n✅ Credential loader is working")
