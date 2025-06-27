import os
import re
from pathlib import Path

def define_env(env):
    """
    Definisce le macro personalizzate per MkDocs
    """
    
    @env.macro
    def knowledge_base_articles():
        """
        Genera un elenco di tutti gli articoli nella knowledge base
        """
        docs_path = Path("docs/knowledge-base")
        articles = []
        
        # Trova tutti i file markdown nella directory knowledge-base
        for file_path in docs_path.glob("*.md"):
            if file_path.name == "index.md":
                continue
                
            # Leggi il titolo dall'articolo
            title = None
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Cerca il primo heading H1
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1)
                    else:
                        # Fallback al nome del file
                        title = file_path.stem.replace('_', ' ').title()
            except Exception:
                title = file_path.stem.replace('_', ' ').title()
            
            # Crea il link relativo
            link = f"{file_path.name}".replace('.md', '')
            articles.append((title, link))
        
        # Ordina alfabeticamente per titolo
        articles.sort(key=lambda x: x[0].lower())
        
        # Genera l'HTML per la lista
        html = "<ul class=\"knowledge-base-list\">\n"
        for title, link in articles:
            html += f"  <li><a href=\"{link}\">{title}</a></li>\n"
        html += "</ul>"
        
        return html
