---
name: wheatomics
description: Access the WheatOmics wheat multi-omics bioinformatics database (https://wheatomics.sdau.edu.cn) via its REST API. Provides gene details, coexpression networks, expression profiles, PPI networks, sequence retrieval, homolog search, synteny analysis, literature search, primer design, and more. Use when Codex needs to query wheat genomics data, retrieve gene sequences or annotations, analyze coexpression/PPI networks, search homologs or synteny across Triticeae species, design SNP primers, or look up wheat literature. Supports IWGSC v1/v2/v3 gene IDs.
---

# WheatOmics Skill

Access the WheatOmics wheat multi-omics database REST API at `https://wheatomics.sdau.edu.cn/api`.

Base URL: `https://wheatomics.sdau.edu.cn/api`
API docs: `https://wheatomics.sdau.edu.cn/api/docs`

All endpoints return JSON. A `curl` wrapper is provided at `scripts/wheatomics.py` for convenient querying.

## Usage pattern

1. Identify the data domain (genes, expression, coexpression, PPI, sequences, homologs, synteny, literature, tasks).
2. Check `references/api_reference.md` for detailed endpoint schemas, parameter meanings, and response formats.
3. Use `python3 scripts/wheatomics.py <endpoint> [params...]` to query. The script prints formatted JSON.
4. For multi-gene queries, join gene IDs with commas (or spaces for batch sequence).

## API domains

### Genes
- `GET /api/genes/detail/{gene_id}` — Gene detail: description, chromosome, protein length, MW, pI, annotations, JBrowse/Ensembl links. Supports IWGSC v1/v2/v3.
- `GET /api/genes/functions/search?ID=` — Search gene function annotations. Modes: genomic interval (`chr5A:100000-200000`), gene ID, or PFAM domain (`PF` prefix).
- `GET /api/genes/known/search?gene_id=` — Search known/characterized genes with phenotypes and references.
- `GET /api/genes/known/{gene_id}` — Get a specific known gene by clone ID or gene ID.
- `POST /api/genes/known` — Submit a new known gene entry.
- `PUT /api/genes/known/{clone_id}` — Update a known gene entry.

### Expression
- `GET /api/expression/projects` — List all expression projects grouped by category (Tissue, Abiotic, Biotic, Development).
- `GET /api/expression/query?gene_ids=&project=` — Query expression values with SD error bars for genes in a project.

### Networks (Coexpression & PPI)
- `GET /api/coexpression/databases` — List available coexpression databases.
- `GET /api/coexpression/query?gene_ids=&database=&filter_value=` — Query coexpression pairs by PCC threshold or mutual rank.
- `GET /api/coexpression/network?gene_ids=&database=&pcc_threshold=` — Build network graph (nodes + edges) for visualization.
- `GET /api/ppi/query?gene_ids=&table=&min_score=` — Query protein-protein interaction pairs.

### Sequences
- `GET /api/sequence/by-gene?gene_id=&gene_db=&protein_db=` — Fetch CDS and protein FASTA for a gene.
- `GET /api/sequence/batch?ID=&database=` — Batch FASTA retrieval for multiple genes (space-separated).
- `GET /api/sequence/by-interval?region=&database=` — Extract genomic DNA from a chromosome interval (max 5 Mb). Region format: `chr1A:100000-200000`.
- `GET /api/preblast?ID=&blastp_species=` — Get precomputed BLAST results for a gene against a species.
- `GET /api/novabrowse?id=` — Run Novabrowse for genome browser visualization.

### Comparative Genomics
- `GET /api/homologs/triticeae?gene_id=&type=` — Find homologs across Triticeae species (Chinese Spring, durum, wild emmer, etc.).
- `GET /api/homologs/wheat-rice-arabidopsis?gene_id=` — Wheat-rice-Arabidopsis ortholog triplets.
- `GET /api/id-conversion?gene_id=&from=&to=` — Convert gene IDs between IWGSC versions (v1/v2/v3) and other formats.
- `GET /api/synteny/search?ID=&table=` — Search syntenic blocks. Input: genomic interval or gene ID.

### Literature
- `GET /api/literature/search?keyword=&tag=&page=&page_size=` — Search wheat literature indexed in the database.
- `GET /api/literature/tags` — Get popular literature tags.

### Tasks (async POST)
- `POST /api/tasks/primer-design` — Submit a primer design job (CAPS/KASP). See reference for request schema.
- `POST /api/tasks/synteny-figure` — Submit a synteny figure rendering job. See reference for request schema.

### Meta
- `GET /api/about` — Get API name, version, docs URL.
- `GET /api/health` — Health check.

## Gene ID formats

WheatOmics supports IWGSC gene IDs in three annotation versions:
- **v1**: `Traes_5AL_XXXXXXXX` (older, underscore-separated)
- **v2**: `TraesCS5A02G391700` (most common)
- **v3**: Similar to v2 with updated annotation

Use `id-conversion` to convert between versions.

## Important constraints

- Sequence by interval: max 5,000,000 bp range.
- Batch sequence uses **spaces** (not commas) between gene IDs.
- All other multi-gene endpoints use **commas**.
- Gene sequence lookup auto-appends `.1` suffix if absent.
- Coexpression `filter_value`: decimal (e.g., 0.8) = PCC threshold | integer (e.g., 5) = mutual rank.
- Synteny input accepts both gene IDs and genomic intervals.

## When results are large

For large response payloads (e.g., expression matrices, coexpression networks), summarize key findings rather than dumping raw JSON. Focus on:
- Number of records returned
- Top hits with scores/values
- Notable patterns or outliers

## Helper script

```bash
# Basic query
python3 scripts/wheatomics.py genes/detail/TraesCS5A02G391700

# With query params
python3 scripts/wheatomics.py coexpression/query gene_ids=TraesCS5A02G391700,TraesCS5B02G123400 database=wheat_expv1 filter_value=0.8

# POST request with JSON body file
python3 scripts/wheatomics.py tasks/primer-design --data @payload.json

# List endpoints
python3 scripts/wheatomics.py --list
```

## Reference

See `references/api_reference.md` for complete endpoint schemas with all parameters, types, defaults, and example responses.
