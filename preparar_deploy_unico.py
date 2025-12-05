"""
Prepara uma estrutura unificada para deploy no Netlify
Organiza as 3 tabelas em um unico site
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

# Pasta de deploy - aponta para o worktree do GitHub Pages
DEPLOY_DIR = Path(r"C:\Users\compr\.claude-worktrees\precos_project\github-pages-deploy")

def preparar_estrutura():
    """Cria estrutura de pastas para deploy unico"""

    print("="*60)
    print("PREPARANDO ESTRUTURA PARA DEPLOY GITHUB PAGES")
    print("="*60)

    # Verifica se o diretório existe
    if not DEPLOY_DIR.exists():
        print(f"\n[ERRO] Diretorio nao encontrado: {DEPLOY_DIR}")
        return

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

    # Copia o App de Pedidos
    app_origem = BASE_DIR / "App Pedidos" / "app_pedidos.html"
    app_destino_dir = DEPLOY_DIR / "app"
    app_destino_dir.mkdir(exist_ok=True)
    app_destino = app_destino_dir / "index.html"

    if app_origem.exists():
        shutil.copy2(app_origem, app_destino)
        print(f"[OK] Copiado: App Pedidos -> app/index.html")
    else:
        print(f"[AVISO] Nao encontrado: {app_origem}")

    # Copia o index.html principal para a raiz
    index_origem = BASE_DIR / "deploy_netlify_site" / "index.html"
    index_destino = DEPLOY_DIR / "index.html"

    if index_origem.exists():
        shutil.copy2(index_origem, index_destino)
        print(f"[OK] Copiado: index.html principal -> raiz")
    else:
        print(f"[AVISO] Nao encontrado: {index_origem}")

    print("\n" + "="*60)
    print("ESTRUTURA PRONTA PARA GITHUB PAGES!")
    print("="*60)
    print(f"\nPasta: {DEPLOY_DIR}")
    print("\nEstrutura:")
    print("  /app/index.html      (App de Pedidos)")
    print("  /ata/index.html      (Tabela ATA)")
    print("  /birigui/index.html  (Tabela BIRIGUI)")
    print("  /prudente/index.html (Tabela PRUDENTE)")
    print("\nLinks diretos:")
    print("  https://ltpsx.github.io/mac-tabelas-precos/app/")
    print("  https://ltpsx.github.io/mac-tabelas-precos/ata/")
    print("  https://ltpsx.github.io/mac-tabelas-precos/birigui/")
    print("  https://ltpsx.github.io/mac-tabelas-precos/prudente/")

if __name__ == "__main__":
    preparar_estrutura()
