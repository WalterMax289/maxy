import wikipedia
import re
from typing import List, Dict, Any

class KnowledgeSynthesizer:
    @staticmethod
    def get_keywords(query: str) -> List[str]:
        noise = ['is', 'who', 'the', 'of', 'what', 'was', 'were', 'tell', 'me', 'about', 'how', 'does', 'are']
        critical_titles = ['pm', 'cm', 'ceo', 'cfo', 'cto', 'md', 'mp', 'mla']
        words = re.findall(r'\b\w+\b', query.lower())
        return [w for w in words if (w in critical_titles or (w not in noise and len(w) > 2))]

    @staticmethod
    def score_relevance(query: str, title: str, body: str) -> float:
        keywords = KnowledgeSynthesizer.get_keywords(query)
        if not keywords: return 0.5
        content = (title + " " + body).lower()
        matches = sum(1 for kw in keywords if kw in content)
        identity_keywords = ['who is', 'who was', 'identity', 'person', 'pm of', 'president of', 'ceo of', 'chief minister of', 'chief of']
        msg_lower = query.lower()
        is_identity = any(ik in msg_lower for ik in identity_keywords)
        
        if is_identity:
            recency_indicators = ['current', 'incumbent', 'serving as', 'holds the position', 'is currently the', 'presently', 'now']
            if any(ri in content for ri in recency_indicators): matches += 2
            historical_indicators = ['former', 'ex-', 'past', 'who was', 'predecessor', 'served as', 'between', 'during']
            if any(hi in content for hi in historical_indicators): matches -= 1
            if re.search(r'\b(19|20)[0-9]{2}[\-–](19|20)[0-9]{2}\b', content):
                if not any(ri in content for ri in recency_indicators): matches -= 1

            names_in_query = re.findall(r'\b[A-Z][a-z]+\b', query)
            if names_in_query:
                content_lower = content.lower()
                name_matches = sum(1 for name in names_in_query if name.lower() in content_lower)
                query_full_name = " ".join(names_in_query).lower()
                title_lower = title.lower().strip()
                if query_full_name == title_lower: matches += 15
                elif query_full_name in title_lower: matches += 5
                if name_matches == 0: return 0.01
                matches += name_matches
        
        score = matches / (len(keywords) + 1)
        if is_identity:
            news_indicators = [':', '?', 'breaking', 'live', 'update', 'latest', 'counters', 'claims', 'vs', 'opinion', 'watch', 'video']
            if any(ni in title.lower() for ni in news_indicators): score *= 0.3
            title_matches = sum(1 for kw in keywords if kw in title.lower())
            if title_matches >= 2: score += 0.2
            if "wikipedia" in title.lower() or "britannica" in title.lower() or "biography" in title.lower(): score += 0.4
        
        return min(1.0, max(0.01, score))

def debug_search(query):
    print(f"DEBUGGING QUERY: {query}")
    wiki_searches = wikipedia.search(query, results=5)
    print(f"Search Results: {wiki_searches}")
    
    candidates = []
    for res in wiki_searches:
        try:
            page = wikipedia.page(res, auto_suggest=False)
            score = KnowledgeSynthesizer.score_relevance(query, page.title, page.summary)
            print(f"CANDIDATE: {page.title}")
            print(f"  Score: {score}")
            print(f"  Summary Length: {len(page.summary)}")
            candidates.append({
                'title': page.title,
                'score': score,
                'summary': page.summary
            })
        except Exception as e:
            print(f"  Error for {res}: {e}")

    candidates.sort(key=lambda x: x['score'], reverse=True)
    if candidates:
        print(f"\nWINNER: {candidates[0]['title']} (Score: {candidates[0]['score']})")

if __name__ == "__main__":
    debug_search("who is mahatma gandhi")
