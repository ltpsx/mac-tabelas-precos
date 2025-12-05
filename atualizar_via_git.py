"""
Script para atualizar e publicar via GitHub Pages
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Configura encoding UTF-8 para o console Windows
if sys.platform == "win32":
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

BASE_DIR = Path(__file__).parent


def executar(comando, descricao=""):
    """Executa comando e retorna True se sucesso"""
    if descricao:
        print(f"\n{descricao}")

    resultado = subprocess.run(
        comando,
        shell=True,
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if resultado.stdout:
        print(resultado.stdout)

    if resultado.returncode != 0:
        if resultado.stderr:
            print(f"[ERRO] {resultado.stderr}")
        return False

    return True


def main():
    print("\n" + "=" * 60)
    print("ATUALIZACAO AUTOMATICA VIA GITHUB PAGES")
    print("=" * 60)
    print(f"Diretorio: {BASE_DIR}")

    # 1. Exportar e gerar HTMLs
    print("\n[1/3] Exportando dados e gerando HTMLs...")
    if not executar("python executar_todas_exportacoes.py"):
        print("\n[ERRO] Falha na exportacao")
        sys.exit(1)

    # 2. Preparar deploy
    print("\n[2/3] Preparando estrutura de deploy...")
    if not executar("python preparar_deploy_unico.py"):
        print("\n[ERRO] Falha na preparacao")
        sys.exit(1)

    # 3. Git commit e push
    print("\n[3/3] Enviando para GitHub...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add arquivos
    executar("git add docs/", "Adicionando arquivos ao Git...")

    # Commit
    commit_msg = f"Atualizacao automatica - {now}"
    executar(f'git commit -m "{commit_msg}"', "Criando commit...")

    # Push
    if executar("git push", "Enviando para GitHub..."):
        print("\n" + "=" * 60)
        print("PUBLICACAO INICIADA NO GITHUB PAGES!")
        print("=" * 60)
        print("\nAguarde 1-2 minutos para o GitHub Pages processar")
        print("\nURLs:")
        print("  App: https://ltpsx.github.io/mac-tabelas-precos/app/")
        print("  ATA: https://ltpsx.github.io/mac-tabelas-precos/ata/")
        print("  Birigui: https://ltpsx.github.io/mac-tabelas-precos/birigui/")
        print("  Prudente: https://ltpsx.github.io/mac-tabelas-precos/prudente/")
        print("\n" + "=" * 60)
    else:
        print("\n[ERRO] Falha no push para GitHub")
        print("\nPossiveis causas:")
        print("  - Git nao configurado")
        print("  - Repositorio nao conectado")
        print("  - Sem permissao de escrita")
        print("\nConsulte: CONFIGURAR_GITHUB.md")
        sys.exit(1)


if __name__ == "__main__":
    main()
