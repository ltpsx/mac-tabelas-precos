# Sistema de Tabelas de Precos - MAC Atacado

Sistema automatizado para exportacao e publicacao de tabelas de precos e app de pedidos (deploy via GitHub Pages).

## Links ativos
- App de Pedidos: https://ltpsx.github.io/mac-tabelas-precos/app/
- Tabela ATA: https://ltpsx.github.io/mac-tabelas-precos/ata/
- Tabela BIRIGUI: https://ltpsx.github.io/mac-tabelas-precos/birigui/
- Tabela PRUDENTE: https://ltpsx.github.io/mac-tabelas-precos/prudente/

## Automacao
Este repositorio usa GitHub Actions para publicar no GitHub Pages. Os arquivos sao atualizados automaticamente quando ha push na branch `main`.

## Estrutura
```
deploy_netlify_site/        # pasta de artefatos publicada no GitHub Pages
├── index.html              # Pagina principal
├── app/                    # App de Pedidos
├── ata/                    # Tabela ATA
├── birigui/                # Tabela BIRIGUI
└── prudente/               # Tabela PRUDENTE
```

## Atualizacao
Para atualizar os dados:
1. Execute o script de exportacao localmente
2. Faca commit e push das alteracoes
3. GitHub Actions publica automaticamente no GitHub Pages

---
MAC Atacado - Sistema de Gestao de Precos
