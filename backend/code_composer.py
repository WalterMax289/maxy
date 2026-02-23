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
        
        # Determine language specific patterns
        is_web = language.lower() in ['html', 'css', 'js', 'javascript']
        
        for res in results:
            body = res.get('body', '')
            title = res.get('title', '')
            content = title + "\n" + body
            
            # 1. Try to extract content between backticks (markdown blocks)
            snippets = re.findall(r'```(?:' + language + r')?\n(.*?)\n```', content, re.DOTALL | re.IGNORECASE)
            
            # 2. If no markdown blocks, look for language-specific structures
            if not snippets:
                if language.lower() == 'python':
                    py_matches = re.findall(r'((?:def|class)\s+\w+.*?)(?=\n\w|\Z)', content, re.DOTALL)
                    if not py_matches:
                        py_matches = re.findall(r'def\s+\w+\(.*?\):.*?(?=\s+def|\s+class|\Z)', content, re.DOTALL)
                    snippets = py_matches
                elif language.lower() in ['javascript', 'js']:
                    js_matches = re.findall(r'(?:function\s+\w+\(|const\s+\w+\s*=|let\s+\w+\s*=|var\s+\w+\s*=).*?\}', content, re.DOTALL)
                    snippets = js_matches
                elif language.lower() == 'html':
                    html_matches = re.findall(r'<(?:div|section|header|footer|nav|main|html|body|head).*?>.*?</(?:div|section|header|footer|nav|main|html|body|head)>', content, re.DOTALL | re.IGNORECASE)
                    snippets = html_matches
                elif language.lower() == 'css':
                    css_matches = re.findall(r'[.#\w\s,-]+?\s*\{[^{}]*?\}', content, re.DOTALL)
                    snippets = css_matches

            # 3. Process found snippets
            for snip in snippets:
                snip = snip.strip()
                # Relaxed validation for web languages
                is_valid = CodeComposer.is_actually_code(snip, language) if not is_web else len(snip) > 20
                if is_valid and snip not in seen_snippets:
                    combined_code += snip + "\n\n"
                    seen_snippets.add(snip)
            
            if len(combined_code) > 2500: # Slightly increased limit
                break
        
        if not combined_code:
            # Fallback: if no valid code blocks found, try to extract paragraphs that look like technical explanations or templates
            best_fallback = ""
            for res in results:
                body = res.get('body', '')
                if any(x in body.lower() for x in ['example', 'template', 'snippet', 'tutorial', 'guide']):
                    if len(body) > len(best_fallback):
                        best_fallback = body
            
            if best_fallback:
                return f"I found a technical reference that might help:\n\n{best_fallback}"
            return ""
            
        return f"```{language}\n{combined_code.strip()}\n```"
