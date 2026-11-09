# Infosiga.SP — sinistros de trânsito do Estado de São Paulo (`infosiga`)

O `infosiga-fetcher` coleta os dados abertos do Infosiga.SP, sistema do Departamento Estadual de Trânsito de São Paulo (Detran-SP) sobre sinistros de trânsito no estado, e os converte para o lake em Parquet particionado por ano. O sistema reúne registros de três origens indicadas no dicionário oficial como "PC, PM e PRF", além de campos do próprio Detran-SP e do IBGE.

| Dataset | O que é | Origem | Período | Página |
|---|---|---|---|---|
| `sinistros` | Um registro por sinistro de trânsito: data, local, via, tipo e contagens de veículos e pessoas por gravidade | CSV `sinistros_*` do ZIP de dados do Infosiga | 2014-12-21 a 2026-09-30 (conferido em 2026-11-09) | [sinistros](datasets/sinistros.md) |
| `pessoas` | Uma linha por pessoa envolvida: posição, sexo, idade, gravidade da lesão e dados do óbito | CSV `pessoas_*` do ZIP de dados do Infosiga | 2014-12-21 a 2026-09-30 | [pessoas](datasets/pessoas.md) |
| `veiculos` | Uma linha por veículo envolvido: tipo, marca e modelo, cor, anos de fabricação e do modelo | CSV `veiculos_*` do ZIP de dados do Infosiga | 2014-12-21 a 2026-09-30 | [veiculos](datasets/veiculos.md) |

## Como o Infosiga publica

- O painel [Infosiga.SP](https://infosiga.detran.sp.gov.br/) oferece para download um único ZIP (`dados_infosiga.zip`) com nove CSV (uma tabela por faixa de anos: 2015-2021, 2022-2024 e 2025-2026) e, à parte, um ZIP com o dicionário de dados (três PDF, um por tabela; versão 1.8 de 15/10/2026).
- O painel informa o período disponível (endpoint `minMaxDates`): 2015-01-01 a 2026-09-30 em 2026-11-09. Os arquivos trazem também 11 sinistros de 21 a 31/12/2014.
- O portal consultado não informa licença nem calendário de atualização.
- O fetcher guarda cada versão baixada com a data de coleta no nome (`<arquivo>@AAAAMMDD`). O lake converte a versão mais recente.

## Como os datasets se relacionam

- `sinistros` é a tabela principal; `pessoas` e `veiculos` ligam a ela por `id_sinistro`, e `pessoas` liga a `veiculos` por `id_veiculo` (nulo para pessoas sem veículo, como pedestres).
- Nem todo sinistro tem pessoas ou veículos registrados nas outras tabelas: na conversão conferida, 981.184 dos 1.450.961 sinistros têm pessoas e 969.834 têm veículos.

## Quebras que valem para mais de um conjunto

| Desde | Mudança | Afeta |
|---|---|---|
| 2019-01 | Os arquivos passam a incluir sinistros não fatais e notificações; de 2015 a 2018 só há sinistros fatais | `sinistros`, `pessoas`, `veiculos` |

Todas as colunas chegam ao lake como texto (datas `dd/mm/aaaa`, coordenadas com vírgula decimal).
