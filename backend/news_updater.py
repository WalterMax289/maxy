import logging
import json
import os
from datetime import datetime
from ddgs import DDGS

logger = logging.getLogger(__name__)

class WorldNewsUpdater:
    """Manages fetching and formatting global news updates"""
    
    @staticmethod
    def fetch_latest_news(max_results=5):
        """Fetch the latest global headlines using DuckDuckGo Search"""
        try:
            with DDGS() as ddgs:
                # Query for top news
                news_results = list(ddgs.text("top world news headlines today", max_results=max_results))
                
                updates = []
                for res in news_results:
                    updates.append({
                        "title": res.get("title", "Global News Update"),
                        "date": datetime.now().strftime("%B %d, %Y"),
                        "description": res.get("body", "Breaking news from around the world today.")
                    })
                return updates
        except Exception as e:
            logger.error(f"Error fetching news with DDGS: {e}")
            return []

    @staticmethod
    def update_json_file():
        """Fetch news and overwrite updates.json"""
        try:
            updates = WorldNewsUpdater.fetch_latest_news()
            
            if not updates:
                logger.warning("No news updates fetched, skipping file write.")
                return False
                
            updates_file = os.path.join(os.path.dirname(__file__), "updates.json")
            
            with open(updates_file, 'w', encoding='utf-8') as f:
                json.dump({"updates": updates}, f, indent=4)
                
            logger.info(f"Successfully updated {updates_file} with {len(updates)} stories.")
            return True
        except Exception as e:
            logger.error(f"Error updating updates.json: {e}")
            return False

if __name__ == "__main__":
    # Test run
    logging.basicConfig(level=logging.INFO)
    WorldNewsUpdater.update_json_file()
