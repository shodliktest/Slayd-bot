"""
RAM Cache Management System
Thread-safe caching with TTL and automatic cleanup
"""
import asyncio
import threading
import time
from typing import Any, Optional, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Global cache storage
_RAM: Dict[str, Any] = {}
_CACHE_METADATA: Dict[str, Dict] = {}  # Stores TTL and access time
_LOCK = threading.Lock()

# Cache configuration
MAX_SIZE_MB = 450
CLEANUP_INTERVAL = 900  # 15 minutes
DEFAULT_TTL = 48 * 3600  # 48 hours


def get(key: str) -> Optional[Any]:
    """Get value from cache"""
    with _LOCK:
        if key in _RAM:
            # Update last access time
            if key in _CACHE_METADATA:
                _CACHE_METADATA[key]['last_access'] = time.time()
            return _RAM[key]
        return None


def set(key: str, value: Any, ttl: Optional[int] = None) -> None:
    """Set value in cache with optional TTL (seconds)"""
    with _LOCK:
        _RAM[key] = value
        _CACHE_METADATA[key] = {
            'created': time.time(),
            'last_access': time.time(),
            'ttl': ttl or DEFAULT_TTL,
            'size_estimate': len(str(value))  # Rough size estimate
        }
        logger.debug(f"Cache SET: {key} (TTL: {ttl or DEFAULT_TTL}s)")


def delete(key: str) -> bool:
    """Delete key from cache"""
    with _LOCK:
        if key in _RAM:
            del _RAM[key]
            if key in _CACHE_METADATA:
                del _CACHE_METADATA[key]
            logger.debug(f"Cache DELETE: {key}")
            return True
        return False


def clear() -> None:
    """Clear all cache"""
    with _LOCK:
        _RAM.clear()
        _CACHE_METADATA.clear()
        logger.info("Cache cleared")


def get_stats() -> Dict:
    """Get cache statistics"""
    with _LOCK:
        total_items = len(_RAM)
        total_size = sum(meta.get('size_estimate', 0) for meta in _CACHE_METADATA.values())
        
        return {
            'total_items': total_items,
            'total_size_mb': total_size / (1024 * 1024),
            'max_size_mb': MAX_SIZE_MB,
            'usage_percent': (total_size / (1024 * 1024)) / MAX_SIZE_MB * 100
        }


def cleanup_expired() -> int:
    """Remove expired items from cache"""
    current_time = time.time()
    removed_count = 0
    
    with _LOCK:
        keys_to_remove = []
        
        for key, meta in _CACHE_METADATA.items():
            # Check if expired
            if current_time - meta['created'] > meta['ttl']:
                keys_to_remove.append(key)
        
        # Remove expired items
        for key in keys_to_remove:
            if key in _RAM:
                del _RAM[key]
            if key in _CACHE_METADATA:
                del _CACHE_METADATA[key]
            removed_count += 1
    
    if removed_count > 0:
        logger.info(f"Cleanup: {removed_count} expired items removed")
    
    return removed_count


def evict_lru(target_size_mb: float) -> int:
    """Evict least recently used items until target size is reached"""
    removed_count = 0
    
    with _LOCK:
        # Sort by last access time
        sorted_items = sorted(
            _CACHE_METADATA.items(),
            key=lambda x: x[1]['last_access']
        )
        
        current_size = sum(meta.get('size_estimate', 0) for meta in _CACHE_METADATA.values())
        current_size_mb = current_size / (1024 * 1024)
        
        for key, meta in sorted_items:
            if current_size_mb <= target_size_mb:
                break
            
            item_size = meta.get('size_estimate', 0)
            
            if key in _RAM:
                del _RAM[key]
            if key in _CACHE_METADATA:
                del _CACHE_METADATA[key]
            
            current_size_mb -= item_size / (1024 * 1024)
            removed_count += 1
    
    if removed_count > 0:
        logger.info(f"LRU Eviction: {removed_count} items removed")
    
    return removed_count


async def cleanup_loop():
    """Background task to cleanup expired cache items"""
    logger.info("Cache cleanup loop started")
    
    while True:
        try:
            await asyncio.sleep(CLEANUP_INTERVAL)
            
            # Remove expired items
            cleanup_expired()
            
            # Check cache size and evict if needed
            stats = get_stats()
            if stats['usage_percent'] > 90:
                logger.warning(f"Cache usage high: {stats['usage_percent']:.1f}%")
                evict_lru(MAX_SIZE_MB * 0.8)  # Reduce to 80%
            
        except Exception as e:
            logger.error(f"Error in cleanup loop: {e}")


async def midnight_flush_loop(bot):
    """Background task to flush cache at midnight"""
    logger.info("Midnight flush loop started")
    
    while True:
        try:
            # Calculate seconds until next midnight
            now = datetime.now()
            tomorrow = now + timedelta(days=1)
            midnight = datetime.combine(tomorrow.date(), datetime.min.time())
            seconds_until_midnight = (midnight - now).total_seconds()
            
            await asyncio.sleep(seconds_until_midnight)
            
            # Flush all data at midnight
            logger.info("Midnight flush: saving all data...")
            from . import tg_db
            await tg_db.flush_all()
            
            # Cleanup old cache
            cleanup_expired()
            
            logger.info("Midnight flush completed")
            
        except Exception as e:
            logger.error(f"Error in midnight flush: {e}")
            await asyncio.sleep(3600)  # Retry in 1 hour


# Specialized cache functions for different data types

def get_content(content_id: str) -> Optional[Dict]:
    """Get generated content from cache"""
    return get(f"content:{content_id}")


def set_content(content_id: str, content: Dict, ttl: int = DEFAULT_TTL) -> None:
    """Cache generated content"""
    set(f"content:{content_id}", content, ttl)


def get_user_history(user_id: int) -> Optional[list]:
    """Get user generation history"""
    return get(f"user_history:{user_id}")


def set_user_history(user_id: int, history: list, ttl: int = 7200) -> None:
    """Cache user history (2 hours TTL)"""
    set(f"user_history:{user_id}", history, ttl)


def get_web_search_results(query: str) -> Optional[Dict]:
    """Get cached web search results"""
    return get(f"search:{query}")


def set_web_search_results(query: str, results: Dict, ttl: int = 3600) -> None:
    """Cache web search results (1 hour TTL)"""
    set(f"search:{query}", results, ttl)
