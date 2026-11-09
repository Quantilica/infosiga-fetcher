# infosiga-fetcher

[![CI](https://github.com/Quantilica/infosiga-fetcher/actions/workflows/test.yml/badge.svg)](https://github.com/Quantilica/infosiga-fetcher/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Coletor e conversor Lake Hive para dados abertos de **Sistema de Informações Gerenciais de Sinistros de Trânsito de SP (INFOSIGA-SP)** (`infosiga`), parte do ecossistema [Quantilica](https://quantilica.com).

## Instalação

### Via CLI Quantilica (recomendado)

```bash
quantilica install infosiga
```

Para instalar com suporte à conversão Parquet Lake:

```bash
quantilica install infosiga --extra analysis
```

### Como biblioteca Python

```bash
uv add infosiga-fetcher --index https://index.quantilica.com/simple/
```

Com o extra de análise analítica:

```bash
uv add 'infosiga-fetcher[analysis]' --index https://index.quantilica.com/simple/
```

## Uso via CLI

```bash
# Listar conjuntos disponíveis
quantilica infosiga list

# Verificar novos arquivos e frescor
quantilica infosiga check

# Sincronizar arquivos para o diretório local bruto
quantilica infosiga sync -o /data/infosiga

# Converter acervo bruto para o Universal Hive Parquet Lake
quantilica infosiga convert /data/infosiga /data/lake
```

## Documentação dos dados

O que cada dataset contém, de onde vem, como chega ao lake e os cuidados de uso: [docs/README.md](docs/README.md).

## Licença

Distribuído sob licença MIT. Consulte [LICENSE](LICENSE) para mais detalhes.
