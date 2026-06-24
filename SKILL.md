---
name: wheatomics
description: Access the WheatOmics wheat multi-omics bioinformatics database (https://wheatomics.sdau.edu.cn) via its REST API. Provides gene details, coexpression networks, expression profiles, PPI networks, sequence retrieval, homolog search, synteny analysis, Triticeae papers, primer design, and more. Use when Codex needs to query wheat genomics data, retrieve gene sequences or annotations, analyze coexpression/PPI networks, search homologs or synteny across Triticeae species, design SNP primers, or search Triticeae papers. Supports IWGSC v1/v2/v3 gene IDs.
---

# WheatOmics Skill

Access the WheatOmics wheat multi-omics database REST API at `https://wheatomics.sdau.edu.cn/api`.

Base URL: `https://wheatomics.sdau.edu.cn/api`
API docs: `https://wheatomics.sdau.edu.cn/api/docs`

All endpoints return JSON. A `curl` wrapper is provided at `scripts/wheatomics.py` for convenient querying.

## Usage pattern

1. Identify the data domain (genes, expression, coexpression, PPI, sequences, homologs, synteny, Triticeae papers, tasks).
2. Check `references/api_reference.md` for detailed endpoint schemas, parameter meanings, and response formats.
3. Use `python3 scripts/wheatomics.py <endpoint> [params...]` to query. The script prints formatted JSON.
4. For multi-gene queries, join gene IDs with commas (or spaces for batch sequence).

## API domains

### Genes
- `GET /api/genes/detail/{gene_id}` — Gene detail: description, chromosome, protein length, MW, pI, annotations, JBrowse/Ensembl links. Supports IWGSC v1/v2/v3.
- `GET /api/genes/functions/pfam?ID=&table=` — PfamSearch: search genes by PFAM domain ID (e.g., `PF00319`). Tables: `Genefunc_table` / `Genefunc_IWGSC03G_table`.
- `GET /api/genes/functions/interval?ID=&table=` — IntervalTool: search genes by chromosome interval (e.g., `chr5A:587000000..587200000`). Tables: `Genefunc_table` / `Genefunc_IWGSC03G_table`.
- `GET /api/genes/functions/tables` — List available gene function database tables and their descriptions.
- `GET /api/genes/known/search?searchid=` — Search known/characterized genes with phenotypes and references.
- `GET /api/genes/known/all` — List all known/characterized genes.
- `GET /api/genes/known/by-chromosome/{chromosome}` — List known genes on a specific chromosome (e.g., `5A`, `chr5A`).
- `GET /api/genes/known/{gene_id}` — Get a specific known gene by clone ID or gene ID.

### Expression
- `GET /api/expression/projects` — List all expression projects grouped by category (Tissue, Abiotic, Biotic, Development).
- `GET /api/expression/query?gene_ids=&project=` — Query expression values with SD error bars for genes in a project. 支持 v1/v2/v3 输入（API 自动将 01G/03G 转换为 02G 后查询）。

### Networks (Coexpression & PPI)
- `GET /api/coexpression/databases` — List available coexpression databases.
- `GET /api/coexpression/query?gene_ids=&database=&filter_value=` — Query coexpression pairs by PCC threshold or mutual rank.
- `GET /api/ppi/query?gene_ids=&table=&min_score=` — wheatPPI: 查询蛋白互作（CF-MS 评分）。仅支持中国春 02G 转录本 ID（需加 `.1` 后缀），不支持 eggNOG ID。评分阈值: 0.5（高置信）/ 0.2（中等）/ 0（全部）。

### Sequences
- `GET /api/sequence/by-gene?searchid=&gene_db=&protein_db=` — Fetch CDS and protein FASTA for a gene.
- `GET /api/sequence/batch?ID=&database=` — Batch FASTA retrieval for multiple genes (space-separated).
- `GET /api/sequence/by-interval?region=&database=` — Extract genomic DNA from a chromosome interval (max 5 Mb). Region format: `chr{Chromosome}_{Variety}:{start}-{end}` (e.g., `chr1A_Fielder:587123000-587124000`).
- `GET /api/preblast?ID=&blastp_species=` — Get precomputed BLAST results for a gene against a species.
- `GET /api/novabrowse?id=` — Run Novabrowse for genome browser visualization.

### BLAST (在线比对)
- `GET /api/blast/databases?program=` — List available BLAST databases. Response includes `protein`, `nucleotide`, `total`, and `categories` (by species/type). `program`: `blastp` / `blastn` / `blastx` / `tblastn` / `tblastx` / 留空=全部。
- `GET /api/blast/status` — Check BLAST environment: blastp/blastn/blastx/tblastn/tblastx + blastdbcmd versions.
- `POST /api/blast/search` — Submit a BLAST search. Request body (form-urlencoded):

  | 参数 | 类型 | 必填 | 默认 | 说明 |
  |------|------|------|------|------|
  | `program` | string | 否 | `blastp` | `blastp`(蛋白→蛋白) / `blastn`(核酸→核酸) / `blastx`(核酸→蛋白) / `tblastn`(蛋白→核酸) / `tblastx`(核酸翻译→蛋白翻译) |
  | `database` | string | **是** | — | 数据库名，多个用逗号分隔 |
  | `query` | string | **是** | — | FASTA 格式的查询序列 |
  | `evalue` | number | 否 | `10.0` | E-value 阈值 |
  | `max_target_seqs` | integer | 否 | `20` | 最多返回的匹配数 |
  > 响应说明：结果无 `hits` 字段，需下载文件查看。始终同时生成 `.tsv`(outfmt 6, 制表符分隔, 易解析) 和 `.txt`(outfmt 0, 含比对信息, 易阅读) 两种格式，下载链接在 `download_url` 数组中，`outfmt` 字段标识已生成的格式。

### Comparative Genomics

### Comparative Genomics
- `GET /api/homologs/triticeae?searchid=&type=` — Find homologs across Triticeae species (Chinese Spring, durum, wild emmer, etc.).
- `GET /api/homologs/wheat-rice-arabidopsis?searchid=` — Wheat-rice-Arabidopsis ortholog triplets.
- `GET /api/id-conversion?ID=&gene_version=` — Convert external gene IDs to IWGSC v1.1 (02G) format. Input: transcript IDs with `.1` suffix, newline-separated (%0D%0A). `gene_version` values: `MIPS_result` (MIPSv2.2, e.g. `Traes_1AS_E6058767A.1`), `TGACv1_result` (TGACv1, e.g. `TRIAE_CS42_6BL_TGACv1_501926_AA1621570.1`), `IWGSCv1_result` (IWGSCv1.0, e.g. `TraesCS6B01G342500.1`). Response includes `code` (mapping class) and `length` fields.
- `GET /api/synteny/search?ID=&table=` — Search syntenic blocks. Input: genomic interval or gene ID.


### Triticeae Papers (文献检索)
- `GET /api/triticeae/papers` — Search Triticeae research papers with filters: `q` (full-text), `gene_name`, `trait_label`, `evidence_type`, `min_confidence`, `review_status`, `ai_tags`, `functional_gene_tags`, `pubmed_keywords`, `new_tags`, `gene_type`, `source_method`, `is_functional_gene`, `functional_gene_flag`, `functional_gene_source`, `function_gene_flag`, `function_gene_tags`, `pub_date_start`, `pub_date_end`, `limit`, `offset`.
- `GET /api/triticeae/papers/{pubmedid}` — Get paper details by PubMed ID.

### Tasks (async POST)
- `POST /api/tasks/primer-design` — Submit a primer design job (CAPS/KASP). See reference for request schema.
- `GET /api/tasks/primer-databases?category=` — List available primer reference databases (all/genome/gene).
- `POST /api/tasks/primer-check` — Check primer specificity against reference genomes.
- `GET /api/tasks/primer-result/{job_id}` — Get primer design/check job result files.
### PrimerServer2 (PCR批量引物设计)


工作流程:
  Step 1 - 收集需求: Agent 询问用户目标基因/区间、扩增方式(全长/区域内)、产物大小范围、参考基因组
  Step 2 - 整理参数给用户确认:
    模板库:      primer_Chinese_Spring2.1.genome
    目标:        Chr3B:569382161-569389178
    Region Type: SEQUENCE_TARGET（区域内）
    产物大小:    150-800 bp
    特异性库:    primer_Chinese_Spring2.1.genome
  Step 3 - 用户确认后提交:

    POST /api/PrimerServer2/jobs
    {
  "app-type": "design",
  "selectTemplate": "primer_Chinese_Spring2.1.genome",
  "template-regions": "Chr3B 569382161 5017 150 800",
  "region_type": "SEQUENCE_TARGET",
  "product_size_min": 150,
  "product_size_max": 800,
  "selected-databases": ["primer_Chinese_Spring2.1.genome"]
}

- `GET /api/PrimerServer2/databases` — List available PCR design/check databases, grouped by category.
- `GET /api/PrimerServer2/config` — Get server configuration limits.
- `GET /api/PrimerServer2/server-info` — Get server info (CPU/memory/tool versions).
- `POST /api/PrimerServer2/jobs` — Submit a PCR primer design job. Key params: `selectTemplate`(模板库), `templateRegions`(目标区域, 格式: `chr start bp minSize maxSize`), `productSizeMin/Max`(产物大小), `selectedDatabases`(特异性库, 默认 `primer_Chinese_Spring2.1.genome`).
- `POST /api/PrimerServer2/jobs/check` — Submit a primer specificity check job.
- `GET /api/PrimerServer2/jobs/{job_id}` — Get job status.
- `DELETE /api/PrimerServer2/jobs/{job_id}` — Cancel/delete a job.
- `GET /api/PrimerServer2/jobs/{job_id}/progress` — Get job progress.
- `GET /api/PrimerServer2/jobs/{job_id}/result` — Get job result JSON.
- `GET /api/PrimerServer2/jobs/{job_id}/result-html` — Legacy: get raw HTML result.
- `GET /api/PrimerServer2/jobs/{job_id}/specificity/{filename}` — Get specificity result file.
- `POST /api/PrimerServer2/jobs/cleanup` — Cleanup old job directories.

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
- `sequence/by-gene` and `sequence/batch` auto-append `.1` suffix if absent.
- `expression/query` 支持 v1/v2/v3 基因 ID（API 自动将 01G/03G 转换为 02G 后查询，转换记录在 `genes_converted` 响应字段中）。
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
python3 scripts/wheatomics.py coexpression/query gene_ids=TraesCS5A02G391700,TraesCS5B02G123400 database=CO_PRJEB25639 filter_value=0.8

# BLAST: 查看可用数据库
python3 scripts/wheatomics.py blast/databases

# BLAST: 蛋白比对
python3 scripts/wheatomics.py blast/search database=Fielder_protein query='>seq\nMSSSTGTPSA...' program=blastp max_target_seqs=5

# BLAST: 查看服务器状态
python3 scripts/wheatomics.py blast/status

# POST request with JSON body file
python3 scripts/wheatomics.py tasks/primer-design --data @payload.json

# List endpoints
python3 scripts/wheatomics.py --list
```

## Reference

See `references/api_reference.md` for complete endpoint schemas with all parameters, types, defaults, and example responses.

- `POST /api/tasks/primer-design` — Submit a primer design job (CAPS/KASP). See reference for request schema.
- `GET /api/tasks/primer-databases?category=` — List available primer reference databases (all/genome/gene).
- `POST /api/tasks/primer-check` — Check primer specificity against reference genomes.
- `GET /api/tasks/primer-result/{job_id}` — Get primer design/check job result files.
### PrimerServer2 (PCR批量引物设计)


工作流程:
  Step 1 - 收集需求: Agent 询问用户目标基因/区间、扩增方式(全长/区域内)、产物大小范围、参考基因组
  Step 2 - 整理参数给用户确认:
    模板库:      primer_Chinese_Spring2.1.genome
    目标:        Chr3B:569382161-569389178
    Region Type: SEQUENCE_TARGET（区域内）
    产物大小:    150-800 bp
    特异性库:    primer_Chinese_Spring2.1.genome
  Step 3 - 用户确认后提交:

    POST /api/PrimerServer2/jobs
    {
  "app-type": "design",
  "selectTemplate": "primer_Chinese_Spring2.1.genome",
  "template-regions": "Chr3B 569382161 5017 150 800",
  "region_type": "SEQUENCE_TARGET",
  "product_size_min": 150,
  "product_size_max": 800,
  "selected-databases": ["primer_Chinese_Spring2.1.genome"]
}

- `GET /api/PrimerServer2/databases` — List available PCR design/check databases, grouped by category.
- `GET /api/PrimerServer2/config` — Get server configuration limits.
- `GET /api/PrimerServer2/server-info` — Get server info (CPU/memory/tool versions).
- `POST /api/PrimerServer2/jobs` — Submit a PCR primer design job. Key params: `selectTemplate`(模板库), `templateRegions`(目标区域, 格式: `chr start bp minSize maxSize`), `productSizeMin/Max`(产物大小), `selectedDatabases`(特异性库, 默认 `primer_Chinese_Spring2.1.genome`).
- `POST /api/PrimerServer2/jobs/check` — Submit a primer specificity check job.
- `GET /api/PrimerServer2/jobs/{job_id}` — Get job status.
- `DELETE /api/PrimerServer2/jobs/{job_id}` — Cancel/delete a job.
- `GET /api/PrimerServer2/jobs/{job_id}/progress` — Get job progress.
- `GET /api/PrimerServer2/jobs/{job_id}/result` — Get job result JSON.
- `GET /api/PrimerServer2/jobs/{job_id}/result-html` — Legacy: get raw HTML result.
- `GET /api/PrimerServer2/jobs/{job_id}/specificity/{filename}` — Get specificity result file.
- `POST /api/PrimerServer2/jobs/cleanup` — Cleanup old job directories.

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
- `sequence/by-gene` and `sequence/batch` auto-append `.1` suffix if absent.
- `expression/query` 支持 v1/v2/v3 基因 ID（API 自动将 01G/03G 转换为 02G 后查询，转换记录在 `genes_converted` 响应字段中）。
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
python3 scripts/wheatomics.py coexpression/query gene_ids=TraesCS5A02G391700,TraesCS5B02G123400 database=CO_PRJEB25639 filter_value=0.8

# BLAST: 查看可用数据库
python3 scripts/wheatomics.py blast/databases

# BLAST: 蛋白比对
python3 scripts/wheatomics.py blast/search database=Fielder_protein query='>seq\nMSSSTGTPSA...' program=blastp max_target_seqs=5

# BLAST: 查看服务器状态
python3 scripts/wheatomics.py blast/status

# POST request with JSON body file
python3 scripts/wheatomics.py tasks/primer-design --data @payload.json

# List endpoints
python3 scripts/wheatomics.py --list
```

## Reference

See `references/api_reference.md` for complete endpoint schemas with all parameters, types, defaults, and example responses.
