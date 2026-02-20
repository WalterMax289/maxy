"""
CodeComposer - Utility for dynamic code and website generation
Provides components for building HTML, CSS, and JS structures
"""

class CodeComposer:
    COMPONENTS = {
        'html': {
            'head': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>''',
            'navbar': '''    <nav class="navbar">
        <div class="logo">{brand}</div>
        <ul class="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>''',
            'hero': '''    <header class="hero">
        <div class="hero-content">
            <h1>Welcome to {title}</h1>
            <p>{description}</p>
            <button class="cta-btn">Get Started</button>
        </div>
    </header>''',
            'features': '''    <section id="services" class="features">
        <h2>Our Services</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <h3>Design</h3>
                <p>Beautiful, modern interfaces.</p>
            </div>
            <div class="feature-card">
                <h3>Development</h3>
                <p>Fast and reliable code.</p>
            </div>
            <div class="feature-card">
                <h3>Analysis</h3>
                <p>Data-driven insights.</p>
            </div>
        </div>
    </section>''',
            'footer': '''    <footer class="footer">
        <p>&copy; 2026 {brand}. All rights reserved.</p>
    </footer>
    <script src="script.js"></script>
</body>
</html>'''
        },
        'css': {
            'common': ''':root {
    --primary: #6366f1;
    --dark: #1f2937;
    --light: #f3f4f6;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Inter', sans-serif; line-height: 1.6; color: var(--dark); }''',
            'navbar': '''.navbar { 
    display: flex; justify-content: space-between; align-items: center; 
    padding: 1rem 5%; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.nav-links { display: flex; list-style: none; gap: 2rem; }
.nav-links a { text-decoration: none; color: var(--dark); font-weight: 500; }''',
            'hero': '''.hero { 
    height: 80vh; display: flex; align-items: center; justify-content: center;
    text-align: center; background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white; padding: 0 20px;
}
.hero h1 { font-size: 3.5rem; margin-bottom: 1rem; }
.cta-btn { 
    padding: 12px 30px; border: none; border-radius: 5px; 
    background: white; color: var(--primary); font-weight: bold; cursor: pointer;
}''',
            'features': '''.features { padding: 5rem 5%; text-align: center; }
.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 3rem; }
.feature-card { padding: 2rem; border-radius: 10px; background: var(--light); transition: transform 0.3s; }
.feature-card:hover { transform: translateY(-5px); }'''
        },
        'js': {
            'smooth_scroll': '''document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});''',
            'scroll_reveal': '''const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('reveal');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('section').forEach(el => observer.observe(el));'''
        }
    }

    @staticmethod
    def build_website(title="My Website", brand="MAXY AI", description="Built with the power of MAXY AI."):
        """Compose a full website from components"""
        html_parts = [
            CodeComposer.COMPONENTS['html']['head'].format(title=title),
            CodeComposer.COMPONENTS['html']['navbar'].format(brand=brand),
            CodeComposer.COMPONENTS['html']['hero'].format(title=title, description=description),
            CodeComposer.COMPONENTS['html']['features'],
            CodeComposer.COMPONENTS['html']['footer'].format(brand=brand)
        ]
        
        css_parts = [
            CodeComposer.COMPONENTS['css']['common'],
            CodeComposer.COMPONENTS['css']['navbar'],
            CodeComposer.COMPONENTS['css']['hero'],
            CodeComposer.COMPONENTS['css']['features']
        ]
        
        js_parts = [
            CodeComposer.COMPONENTS['js']['smooth_scroll'],
            CodeComposer.COMPONENTS['js']['scroll_reveal']
        ]
        
        return {
            'html': '\n'.join(html_parts),
            'css': '\n'.join(css_parts),
            'js': '\n'.join(js_parts)
        }

    @staticmethod
    def build_portfolio(name="John Doe", title="Full Stack Developer"):
        """Specialized portfolio generation"""
        # Simplify for brevity in this response
        return CodeComposer.build_website(
            title=f"{name} - Portfolio",
            brand=name.upper(),
            description=f"Welcome to my professional space. I am a {title}."
        )

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
