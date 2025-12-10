#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera DUAS versões do App de Pedidos ATA PLUS:
1. app_pedidos.html - Com dados embutidos (offline, 2.8MB)
2. app_pedidos_web.html + dados.json - Com dados externos (online, leve)

Para GitHub Pages, usaremos a versão WEB (leve)
"""

import csv
import json
from datetime import datetime
from pathlib import Path
import sys

# Configura encoding UTF-8 para o console Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Define os caminhos
BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR.parent / "Tabela Ata Plus" / "TABPRECOS.csv"
TEMPLATE_EMBUTIDO = BASE_DIR / "template_app_pedidos.html"
TEMPLATE_EXTERNO = BASE_DIR / "template_app_pedidos_externo.html"
SAIDA_EMBUTIDO = BASE_DIR / "app_pedidos.html"
SAIDA_EXTERNO = BASE_DIR / "app_pedidos_web.html"
SAIDA_JSON = BASE_DIR / "dados.json"

print("="*60)
print("GERANDO APLICATIVO DE PEDIDOS ATA PLUS - DUAS VERSÕES")
print("="*60)

# ============================================================
# ETAPA 1: LER E PROCESSAR CSV
# ============================================================
print("\n[1/4] Lendo CSV...")

dados = []
ultima_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M")

with CSV_PATH.open("r", encoding="cp1252", newline="") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        codigo = (row.get("CÓDIGO PRODUTO") or "").strip()
        cod_fab = (row.get("CÓDIGO FABRIC") or "").strip()
        marca = (row.get("MARCA") or "").strip()
        nome = (row.get("COMPLEMENTO") or "").strip()
        estoque = (row.get("ESTOQUE DISPONÍVEL") or "").strip()
        preco = (row.get("PREÇO DE VENDA") or "").strip()

        # Pula linhas vazias
        if not codigo and not nome:
            continue

        dados.append({
            "codigo": codigo,
            "fabric": cod_fab,
            "marca": marca,
            "nome": nome,
            "estoque": estoque,
            "preco": preco
        })

print(f"✅ Total de produtos: {len(dados)}")

# Ordena por nome para facilitar navegação
dados.sort(key=lambda x: x["nome"].upper())

# ============================================================
# ETAPA 2: GERAR VERSÃO COM DADOS EMBUTIDOS (OFFLINE)
# ============================================================
print("\n[2/4] Gerando versão OFFLINE (dados embutidos)...")

if TEMPLATE_EMBUTIDO.exists():
    json_data = json.dumps(dados, ensure_ascii=False, separators=(',', ':'))
    html_embutido = TEMPLATE_EMBUTIDO.read_text(encoding="utf-8")
    html_embutido = html_embutido.replace("__DADOS_PRODUTOS__", json_data)
    html_embutido = html_embutido.replace("__ULTIMA_ATUALIZACAO__", ultima_atualizacao)
    SAIDA_EMBUTIDO.write_text(html_embutido, encoding="utf-8")

    tamanho_mb = SAIDA_EMBUTIDO.stat().st_size / (1024 * 1024)
    print(f"✅ Arquivo: {SAIDA_EMBUTIDO.name}")
    print(f"   Tamanho: {tamanho_mb:.2f} MB")
    print(f"   Produtos: {len(dados)}")
else:
    print(f"⚠️  Template não encontrado: {TEMPLATE_EMBUTIDO}")

# ============================================================
# ETAPA 3: GERAR VERSÃO WEB (DADOS EXTERNOS)
# ============================================================
print("\n[3/4] Gerando versão WEB (dados externos)...")

if TEMPLATE_EXTERNO.exists():
    html_externo = TEMPLATE_EXTERNO.read_text(encoding="utf-8")
    html_externo = html_externo.replace("__ULTIMA_ATUALIZACAO__", ultima_atualizacao)
    SAIDA_EXTERNO.write_text(html_externo, encoding="utf-8")

    tamanho_kb = SAIDA_EXTERNO.stat().st_size / 1024
    print(f"✅ Arquivo HTML: {SAIDA_EXTERNO.name}")
    print(f"   Tamanho: {tamanho_kb:.1f} KB")
else:
    print(f"⚠️  Template não encontrado: {TEMPLATE_EXTERNO}")

# ============================================================
# ETAPA 4: GERAR ARQUIVO JSON SEPARADO
# ============================================================
print("\n[4/4] Gerando arquivo de dados (JSON)...")

json_data = json.dumps(dados, ensure_ascii=False, indent=2)
SAIDA_JSON.write_text(json_data, encoding="utf-8")

tamanho_mb = SAIDA_JSON.stat().st_size / (1024 * 1024)
print(f"✅ Arquivo JSON: {SAIDA_JSON.name}")
print(f"   Tamanho: {tamanho_mb:.2f} MB")
print(f"   Produtos: {len(dados)}")

# ============================================================
# RESUMO FINAL
# ============================================================
print("\n" + "="*60)
print("GERAÇÃO CONCLUÍDA!")
print("="*60)

print("\n📱 VERSÃO OFFLINE (para uso local):")
print(f"   {SAIDA_EMBUTIDO.resolve()}")
print("   - Funciona sem internet")
print("   - Arquivo único (pesado)")
print("   - Ideal para mobile offline")

print("\n🌐 VERSÃO WEB (para GitHub Pages):")
print(f"   {SAIDA_EXTERNO.resolve()}")
print(f"   {SAIDA_JSON.resolve()}")
print("   - Requer internet")
print("   - HTML leve + JSON separado")
print("   - Ideal para deploy online")

print("\n💡 PRÓXIMOS PASSOS:")
print("   1. Para GitHub Pages: use app_pedidos_web.html + dados.json")
print("   2. Para uso offline: use app_pedidos.html")
print("="*60)
