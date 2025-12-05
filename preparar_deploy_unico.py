"""
Prepara estrutura unificada para publicar via GitHub Pages
Organiza as 3 tabelas e o app em um unico site
"""

import shutil
from pathlib import Path
import sys

# Configura encoding UTF-8 para o console Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

BASE_DIR = Path(__file__).parent

# Pasta de deploy dentro do repo principal (publicada no GitHub Pages)
DEPLOY_DIR = Path(__file__).parent / "docs"

def preparar_estrutura():
    """Cria estrutura de pastas para deploy unico"""

    print("="*60)
    print("PREPARANDO ESTRUTURA PARA DEPLOY GITHUB PAGES")
    print("="*60)

    # Garante que a pasta de deploy existe
    DEPLOY_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\nAtualizando estrutura em: {DEPLOY_DIR}")

    # Copia os HTMLs de cada tabela
    tabelas = [
        ("Tabela Ata", "ata"),
        ("Tabela Birigui", "birigui"),
        ("Tabela Prudente", "prudente")
    ]

    for pasta_origem, nome_destino in tabelas:
        origem = BASE_DIR / pasta_origem / "tabela_preco.html"
        destino_dir = DEPLOY_DIR / nome_destino
        destino_dir.mkdir(exist_ok=True)
        destino = destino_dir / "index.html"

        if origem.exists():
            shutil.copy2(origem, destino)
            print(f"[OK] Copiado: {pasta_origem} -> {nome_destino}/index.html")
        else:
            print(f"[AVISO] Nao encontrado: {origem}")

    # Copia o App de Pedidos (versão atualizada)
    app_origem_html = BASE_DIR / "App Pedidos" / "app_pedidos_web.html"
    app_origem_json = BASE_DIR / "App Pedidos" / "dados.json"
    app_destino_dir = DEPLOY_DIR / "app"
    app_destino_dir.mkdir(exist_ok=True)
    app_destino_html = app_destino_dir / "index.html"
    app_destino_json = app_destino_dir / "dados.json"

    if app_origem_html.exists():
        shutil.copy2(app_origem_html, app_destino_html)
        print(f"[OK] Copiado: App Pedidos WEB -> app/index.html")
    else:
        print(f"[AVISO] Nao encontrado: {app_origem_html}")

    if app_origem_json.exists():
        shutil.copy2(app_origem_json, app_destino_json)
        print(f"[OK] Copiado: Dados JSON -> app/dados.json")
    else:
        print(f"[AVISO] Nao encontrado: {app_origem_json}")

    print("\n" + "="*60)
    print("ESTRUTURA PRONTA PARA GITHUB PAGES!")
    print("="*60)
    print(f"\nPasta: {DEPLOY_DIR}")
    print("\nEstrutura:")
    print("  /app/index.html              (App de Pedidos - ATUALIZADO)")
    print("  /app/dados.json              (Dados dos produtos - JSON)")
    print("  /ata/index.html              (Tabela ATA)")
    print("  /birigui/index.html          (Tabela BIRIGUI)")
    print("  /prudente/index.html         (Tabela PRUDENTE)")
    print("\nLinks diretos:")
    print("  https://ltpsx.github.io/mac-tabelas-precos/app/")
    print("  https://ltpsx.github.io/mac-tabelas-precos/ata/")
    print("  https://ltpsx.github.io/mac-tabelas-precos/birigui/")
    print("  https://ltpsx.github.io/mac-tabelas-precos/prudente/")
    print("\n💡 App de Pedidos completo e atualizado (2.8MB)")

if __name__ == "__main__":
    preparar_estrutura()
