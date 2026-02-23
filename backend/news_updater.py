import logging
import json
import os
from datetime import datetime
from ddgs import DDGS

logger = logging.getLogger(__name__)

class WorldNewsUpdater:
    """Manages fetching and formatting global news updates"""
    
    @staticmethod
    def fetch_categorized_news():
        """Fetch professional news and Bengaluru updates using DuckDuckGo News"""
        updates = []
        try:
            with DDGS() as ddgs:
                # 1. Fetch Tech & Industry News (Google News style)
                tech_results = list(ddgs.news("latest technology industry news", max_results=4))
                for res in tech_results:
                    updates.append({
                        "title": res.get("title", "Tech News"),
                        "type": "tech",
                        "date": res.get("date", datetime.now().strftime("%B %d, %Y")),
                        "description": res.get("body", "Latest industry developments.")
                    })
                
                # 2. Fetch Bengaluru Highlights
                bengaluru_results = list(ddgs.news("Bengaluru news highlights", max_results=3))
                for res in bengaluru_results:
                    updates.append({
                        "title": res.get("title", "Bengaluru News"),
                        "type": "bengaluru",
                        "date": res.get("date", datetime.now().strftime("%B %d, %Y")),
                        "description": res.get("body", "Local news flash from Bengaluru.")
                    })
                
                return updates
        except Exception as e:
            logger.error(f"Error fetching categorized news with DDGS: {e}")
            return updates

    @staticmethod
    def update_json_file():
        """Fetch news and overwrite updates.json"""
        try:
            updates = WorldNewsUpdater.fetch_categorized_news()
            
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
