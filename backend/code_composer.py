"""
CodeComposer - Utility for dynamic code and website generation
Provides components for building HTML, CSS, and JS structures
"""

class CodeComposer:
    @staticmethod
    def build_website(title="My Website", brand="MAXY AI", description="Built with the power of MAXY AI."):
        """
        [DEPRECATED] Site building will now be handled via Deep Research synthesis.
        """
        return {
            'html': f"<!-- Deep Research Required for '{title}' -->",
            'css': "/* Deep Research Required */",
            'js': "// Deep Research Required"
        }

    @staticmethod
    def build_portfolio(name="John Doe", title="Full Stack Developer"):
        """
        [DEPRECATED] Portfolio building will now be handled via Deep Research synthesis.
        """
        return CodeComposer.build_website(title=f"{name} - Portfolio")

    @staticmethod
    def is_actually_code(snippet: str, language: str) -> bool:
        """Heuristic to check if a snippet is likely valid code"""
        if not snippet or len(snippet) < 15:
            return False
            
        if language == 'python':
            # Must have typical indentation symbols or specific keywords at start of lines
            has_keywords = any(kw in snippet for kw in ['def ', 'class ', 'import ', 'from ', 'print(', ' = ', 'elif '])
            has_structure = ':' in snippet and ('    ' in snippet or '\t' in snippet or '\n' in snippet)
            return has_keywords or has_structure
            
        return True # Default for other langs

    @staticmethod
    def synthesize_code_from_search(results: list, language: str) -> str:
        """Synthesize a clean code block from search results with robust fallbacks"""
        import re
        
        combined_code = ""
        seen_snippets = set()
        
        for res in results:
            body = res.get('body', '')
            title = res.get('title', '')
            content = title + "\n" + body
            
            # 1. Try to extract content between backticks (markdown blocks)
            snippets = re.findall(r'```(?:' + language + r')?\n(.*?)\n```', content, re.DOTALL)
            
            # 2. If no markdown blocks, look for language-specific structures
            if not snippets:
                if language == 'python':
                    # Look for complete function blocks or class definitions
                    # Matches starting from 'def ' or 'class '
                    py_matches = re.findall(r'((?:def|class)\s+\w+.*?)(?=\n\w|\Z)', content, re.DOTALL)
                    if not py_matches:
                        # Try to find common patterns like 'def foo(): ...' even if not perfectly formatted
                        py_matches = re.findall(r'def\s+\w+\(.*?\):.*?(?=\s+def|\s+class|\Z)', content, re.DOTALL)
                    snippets = py_matches
                elif language in ['javascript', 'js']:
                    js_matches = re.findall(r'(?:function\s+\w+\(|const\s+\w+\s*=|let\s+\w+\s*=|var\s+\w+\s*=).*?\}', content, re.DOTALL)
                    snippets = js_matches

            # 3. Process found snippets
            for snip in snippets:
                snip = snip.strip()
                if CodeComposer.is_actually_code(snip, language) and snip not in seen_snippets:
                    combined_code += snip + "\n\n"
                    seen_snippets.add(snip)
            
            if len(combined_code) > 2000:
                break
        
        if not combined_code:
            # Fallback: if no valid code blocks found, return the most detailed technical result as text
            for res in results:
                body = res.get('body', '')
                if any(x in body.lower() for x in ['implementation', 'algorithm', 'syntax', 'manual']):
                    return f"I found a technical overview for this request:\n\n{body}"
            return ""
            
        return f"```{language}\n{combined_code.strip()}\n```"
