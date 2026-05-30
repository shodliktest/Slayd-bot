"""
Telegram Database System
Uses Telegram channel as database storage
"""
import asyncio
import json
import logging
from typing import Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Global state
_bot = None
_channel_id = None
_index_msg_id = None
_data_cache = {}
_flush_pending = False


async def init(bot, channel_id: int):
    """Initialize database with bot and channel"""
    global _bot, _channel_id
    _bot = bot
    _channel_id = channel_id
    
    logger.info(f"TG DB initialized with channel: {channel_id}")
    
    # Load index
    await _load_index()


async def save_content(content_id: str, data: Dict) -> bool:
    """Save content to database"""
    
    try:
        # Save to cache
        _data_cache[content_id] = data
        
        # Save to Telegram
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        
        file = json_data.encode('utf-8')
        filename = f"{content_id}.json"
        
        msg = await _bot.send_document(
            chat_id=_channel_id,
            document=('file', file, filename),
            caption=f"📄 {content_id}"
        )
        
        # Update index
        await _update_index(content_id, msg.message_id)
        
        logger.info(f"Saved content: {content_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving content: {e}")
        return False


async def get_content(content_id: str) -> Optional[Dict]:
    """Get content from database"""
    
    # Check cache first
    if content_id in _data_cache:
        return _data_cache[content_id]
    
    # Load from Telegram
    try:
        index = await _load_index()
        
        if content_id not in index:
            return None
        
        msg_id = index[content_id]
        
        # Get file from message
        msg = await _bot.forward_message(
            chat_id=_channel_id,
            from_chat_id=_channel_id,
            message_id=msg_id
        )
        
        # Download and parse
        file = await _bot.get_file(msg.document.file_id)
        file_content = await _bot.download_file(file.file_path)
        
        data = json.loads(file_content.read().decode('utf-8'))
        
        # Cache it
        _data_cache[content_id] = data
        
        return data
        
    except Exception as e:
        logger.error(f"Error getting content: {e}")
        return None


async def delete_content(content_id: str) -> bool:
    """Delete content from database"""
    
    try:
        # Remove from cache
        if content_id in _data_cache:
            del _data_cache[content_id]
        
        # Delete from Telegram
        index = await _load_index()
        
        if content_id in index:
            msg_id = index[content_id]
            await _bot.delete_message(_channel_id, msg_id)
            
            # Update index
            del index[content_id]
            await _save_index(index)
        
        logger.info(f"Deleted content: {content_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error deleting content: {e}")
        return False


async def _load_index() -> Dict:
    """Load index from pinned message"""
    global _index_msg_id
    
    try:
        # Get pinned message
        chat = await _bot.get_chat(_channel_id)
        
        if hasattr(chat, 'pinned_message') and chat.pinned_message:
            _index_msg_id = chat.pinned_message.message_id
            
            # Download index file
            file = await _bot.get_file(chat.pinned_message.document.file_id)
            file_content = await _bot.download_file(file.file_path)
            
            index = json.loads(file_content.read().decode('utf-8'))
            return index.get('contents', {})
        
        return {}
        
    except Exception as e:
        logger.error(f"Error loading index: {e}")
        return {}


async def _save_index(index: Dict):
    """Save index to pinned message"""
    global _index_msg_id
    
    try:
        data = {
            'last_updated': datetime.now().isoformat(),
            'contents': index
        }
        
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        file = json_data.encode('utf-8')
        
        # Send new index
        msg = await _bot.send_document(
            chat_id=_channel_id,
            document=('file', file, 'index.json'),
            caption="📌 Database Index"
        )
        
        # Pin it
        await _bot.pin_chat_message(_channel_id, msg.message_id)
        
        # Delete old index
        if _index_msg_id:
            try:
                await _bot.delete_message(_channel_id, _index_msg_id)
            except:
                pass
        
        _index_msg_id = msg.message_id
        
    except Exception as e:
        logger.error(f"Error saving index: {e}")


async def _update_index(content_id: str, msg_id: int):
    """Update index with new content"""
    
    index = await _load_index()
    index[content_id] = msg_id
    await _save_index(index)


async def flush_all():
    """Flush all pending data"""
    logger.info("Flushing all data to Telegram...")
    # Index is already saved on each write
    logger.info("Flush completed")


async def auto_flush_loop():
    """Background task to periodically flush data"""
    logger.info("Auto flush loop started")
    
    while True:
        try:
            await asyncio.sleep(300)  # Every 5 minutes
            # Data is already flushed on write
            
        except Exception as e:
            logger.error(f"Error in auto flush: {e}")
