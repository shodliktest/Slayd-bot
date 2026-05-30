"""
Web Search and Image Finder
Uses Serper API for web search and Unsplash for images
"""
import logging
from typing import List, Dict, Optional
import aiohttp

from config import SERPER_API_KEY, UNSPLASH_ACCESS_KEY

logger = logging.getLogger(__name__)


async def search_web(query: str, num_results: int = 5) -> List[Dict]:
    """Search web for information"""
    
    if not SERPER_API_KEY:
        logger.warning("Serper API key not configured")
        return []
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "q": query,
        "num": num_results
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    
                    for item in data.get('organic', []):
                        results.append({
                            'title': item.get('title', ''),
                            'snippet': item.get('snippet', ''),
                            'link': item.get('link', '')
                        })
                    
                    logger.info(f"Found {len(results)} results for: {query}")
                    return results
                else:
                    logger.error(f"Serper API error: {response.status}")
                    return []
                    
    except Exception as e:
        logger.error(f"Error searching web: {e}")
        return []


async def find_images(keywords: str, count: int = 3) -> List[str]:
    """Find images from Unsplash"""
    
    if not UNSPLASH_ACCESS_KEY:
        logger.warning("Unsplash API key not configured")
        return []
    
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    
    params = {
        "query": keywords,
        "per_page": count,
        "orientation": "landscape"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    images = []
                    
                    for photo in data.get('results', []):
                        images.append(photo['urls']['regular'])
                    
                    logger.info(f"Found {len(images)} images for: {keywords}")
                    return images
                else:
                    logger.error(f"Unsplash API error: {response.status}")
                    return []
                    
    except Exception as e:
        logger.error(f"Error finding images: {e}")
        return []


async def download_image(url: str, filepath: str) -> bool:
    """Download image from URL"""
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(filepath, 'wb') as f:
                        f.write(await response.read())
                    return True
                else:
                    logger.error(f"Failed to download image: {response.status}")
                    return False
                    
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
        return False
