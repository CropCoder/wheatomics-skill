# WheatOmics Skill for Codex CLI

A skill for the [Codex CLI](https://github.com/openai/codex) that provides access to the [WheatOmics](https://wheatomics.sdau.edu.cn) wheat multi-omics bioinformatics database via its REST API.

## Features

- **Gene details**: description, chromosome, protein length, MW, pI, annotations, JBrowse/Ensembl links
- **Expression profiles**: query across 60+ projects (tissue development, abiotic/biotic stress, hormone treatment)
- **Coexpression networks**: PCC-based coexpression pairs from grain and multi-tissue databases
- **PPI networks**: protein-protein interaction pairs
- **Sequence retrieval**: CDS, protein FASTA, batch retrieval, genomic interval extraction
- **Comparative genomics**: Triticeae homologs, wheat-rice-Arabidopsis orthologs, synteny blocks
- **Literature search**: indexed wheat literature with tags
- **Primer design**: CAPS/KASP primer design
- **ID conversion**: IWGSC v1/v2/v3 gene ID conversion

## Installation

```bash
# Install via Codex skill-installer
codex skill install wheatomics
```

Or manually copy the `wheatomics/` directory to `$CODEX_HOME/skills/`.

## Usage

In Codex CLI, trigger by mentioning `$wheatomics` followed by your query:

```
$wheatomics 查一下 TraesCS5A02G391700 的表达量
$wheatomics find coexpression partners for this gene
$wheatomics get the protein sequence
```

## API Base URL

https://wheatomics.sdau.edu.cn/api

API docs: https://wheatomics.sdau.edu.cn/api/docs

## Supported Gene ID Formats

- **v1**: `Traes_5AL_XXXXXXXX`
- **v2**: `TraesCS5A02G391700` (most common)
- **v3**: Similar to v2

## Files

```
wheatomics/
├── SKILL.md                  # Skill definition and workflow
├── scripts/
│   └── wheatomics.py         # curl wrapper for API queries
├── references/
│   └── api_reference.md      # Complete endpoint schemas
└── agents/
    └── openai.yaml           # Agent configuration
```

## Reference

WheatOmics paper: Ma S. et al., *WheatOmics: A platform combining multiple omics data to accelerate functional genomics studies in wheat*, Molecular Plant (2021). doi:10.1016/j.molp.2021.10.006

## License

This skill is provided for use with Codex CLI. The WheatOmics database is developed by Shandong Agricultural University.
