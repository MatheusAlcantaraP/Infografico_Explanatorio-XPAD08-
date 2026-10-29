# Infográfico explanatório: iniciação científica e tecnológica na UNIFEI

Atividade 3 (Visualização explanatória: convencer com dados), tema 7: incentivar estudantes de graduação a participar de projetos de iniciação tecnológica.

O projeto gera, com Python e matplotlib, um infográfico em PNG e PDF a partir de dados públicos da UFES e da UFSJ.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `gerar_infografico.py` | Script que desenha o infográfico e salva o PNG e o PDF |
| `infografico_iniciacao.png` | Infográfico em imagem (gerado pelo script) |
| `infografico_iniciacao.pdf` | Infográfico em PDF, uma página (gerado pelo script) |

## Como rodar

```bash
python -m pip install matplotlib
python gerar_infografico.py
```

Os arquivos `infografico_iniciacao.png` e `infografico_iniciacao.pdf` são criados na mesma pasta do script.

## Fontes dos dados

- UFES: Salazar AD et al. *Iniciação Científica na Universidade Federal do Espírito Santo: egressos e evolução.* Rev. Bras. Pesq. Saúde 22(4):8–14, 2020. doi:10.47456/rbps.v22i4.35453
- UFSJ: Pró-reitoria de Pesquisa e Pós-graduação. *Acompanhamento de egressos do Programa de Iniciação Científica (2015–2023).*
- UNIFEI: Diretoria de Pesquisa, páginas Iniciação Científica e Editais de Pesquisa (consultadas em 28/10/2026).
