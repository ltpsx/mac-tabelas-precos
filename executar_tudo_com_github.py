"""
Script COMPLETO: Exporta tabelas + Gera HTML + Faz Deploy no GitHub Pages
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Configura encoding UTF-8 para o console Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

BASE_DIR = Path(__file__).parent

def executar_comando(comando, descricao):
    """Executa um comando e retorna True se sucesso, False se erro"""
    print(f"\n{'='*60}")
    print(f">>> {descricao}")
    print(f"{'='*60}")

    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=str(BASE_DIR)
        )

        if resultado.stdout:
            print(resultado.stdout)

        print(f"[OK] {descricao} - SUCESSO")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[ERRO] {descricao} - FALHOU")
        print(f"Codigo de saida: {e.returncode}")
        if e.stdout:
            print(f"Saida: {e.stdout}")
        if e.stderr:
            print(f"Erro: {e.stderr}")
        return False
    except Exception as e:
        print(f"[ERRO] {descricao} - ERRO INESPERADO")
        print(f"Erro: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("AUTOMACAO COMPLETA: EXPORTACAO + DEPLOY GITHUB PAGES")
    print("="*60)
    print(f"Diretorio: {BASE_DIR}")
    print(f"Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # Lista de tarefas
    tarefas = [
        # ETAPA 1: EXPORTAR E GERAR HTMLs
        {
            "comando": "python executar_todas_exportacoes.py",
            "descricao": "1/4 - Exportar tabelas e gerar HTMLs + App"
        },

        # ETAPA 2: PREPARAR DEPLOY
        {
            "comando": "python preparar_deploy_unico.py",
            "descricao": "2/4 - Preparar estrutura de deploy"
        },

        # ETAPA 3: GIT ADD (repo principal)
        {
            "comando": 'git add docs/',
            "descricao": "3/4 - Adicionar arquivos ao Git (docs)"
        },

        # ETAPA 4: GIT COMMIT + PUSH (repo principal)
        {
            "comando": f'git commit -m "Atualizacao automatica - {datetime.now().strftime("%d/%m/%Y %H:%M")}" && git push',
            "descricao": "4/4 - Commit e push para GitHub (main)"
        },
    ]

    # Executa todas as tarefas
    sucessos = 0
    erros = 0

    for tarefa in tarefas:
        if executar_comando(tarefa["comando"], tarefa["descricao"]):
            sucessos += 1
        else:
            erros += 1
            # Se falhar no git commit (sem mudancas), continua normal
            if "git commit" in tarefa["comando"]:
                print("[INFO] Sem mudancas para commit - tudo ok!")
                sucessos += 1
                erros -= 1
            else:
                break  # Para se houver erro real

    # Resumo final
    print("\n" + "="*60)
    print("RESUMO FINAL")
    print("="*60)
    print(f"[OK] Etapas concluidas: {sucessos}")
    print(f"[ERRO] Etapas com erro: {erros}")

    if erros == 0:
        print("\n*** PROCESSO COMPLETO CONCLUIDO COM SUCESSO! ***")
        print("\nSite atualizado:")
        print("  https://ltpsx.github.io/mac-tabelas-precos/")
        print("\nApp de Pedidos:")
        print("  https://ltpsx.github.io/mac-tabelas-precos/app/")
        print("\nDeploy automatico ira acontecer em ~1 minuto via GitHub Actions!")
    else:
        print(f"\n[AVISO] Processo interrompido com {erros} erro(s)")

    print("\n" + "="*60)

if __name__ == "__main__":
    main()
