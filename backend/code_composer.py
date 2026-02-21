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
    def synthesize_code_from_search(results: list, language: str) -> str:
        """Synthesize a clean code block from search results"""
        import re
        
        combined_code = ""
        seen_snippets = set()
        
        for res in results:
            body = res.get('body', '')
            # Try to extract content between backticks
            snippets = re.findall(r'```(?:' + language + r')?\n(.*?)\n```', body, re.DOTALL)
            
            if not snippets:
                # Try to find anything that looks like code if no markdown blocks
                if language == 'python':
                    # Look for def or imports
                    py_matches = re.findall(r'(?:def\s+\w+\(|import\s+\w+|from\s+\w+\s+import).*', body)
                    snippets = py_matches
            
            for snip in snippets:
                snip = snip.strip()
                if snip and len(snip) > 20 and snip not in seen_snippets:
                    combined_code += snip + "\n\n"
                    seen_snippets.add(snip)
            
            if len(combined_code) > 1500:
                break
        
        if not combined_code:
            # If no code found, use the first body as a text description
            return ""
            
        return f"```{language}\n{combined_code.strip()}\n```"
