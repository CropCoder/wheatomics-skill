# WheatOmics API Reference

Base URL: `https://wheatomics.sdau.edu.cn/api`
Interactive docs: `https://wheatomics.sdau.edu.cn/api/docs`

## Endpoints

### GET /api/about

**Root**

**Example:**
```bash
curl -X GET "http://localhost:8000/api/about"
```

---

### GET /api/coexpression/databases

**Tags:** Networks

**List Coexpression Databases**

**Example:**
```bash
curl -X GET "http://localhost:8000/api/coexpression/databases"
```

---

### GET /api/coexpression/query

**Tags:** Networks

**Query Coexpression**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gene_ids` | string | Yes | - |  |
| `database` | string, default: CO_PRJEB25639 | No | CO_PRJEB25639 |  |
| `filter_value` | number, default: 0.8 | No | 0.8 |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/coexpression/query?gene_ids=TraesCS5A02G391700&database=CO_PRJEB25639&filter_value=0.9"
```

---

### GET /api/expression/projects

**Tags:** Expression

**Get Expression Projects**

**Example:**
```bash
curl -X GET "http://localhost:8000/api/expression/projects"
```

---

### GET /api/expression/query

**Tags:** Expression

**Query Expression**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gene_ids` | string | Yes | - | Comma separated gene IDs |
| `project` | string, default: PRJEB5314_paired_tbl | No | PRJEB5314_paired_tbl |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/expression/query?gene_ids=TraesCS5A02G391700,TraesCS5A02G391700.1&project=PRJEB5314_paired_tbl"
```

---

### GET /api/genes/detail/{gene_id}

**Tags:** Genes

**Get Gene Detail**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gene_id` | string | Yes | - |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/genes/detail/TraesCS5A02G391700"
```

---

### GET /api/genes/functions/pfam

**PfamSearch:** search genes by PFAM domain ID.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ID` | string | Yes | - | PFAM domain ID (e.g., PF00319) |
| `table` | string, default: Genefunc_table | No | Genefunc_table | Genefunc_table or Genefunc_IWGSC03G_table |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/genes/functions/pfam?ID=PF00319"
```

---

### GET /api/genes/functions/interval

**IntervalTool:** search genes by chromosome interval.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ID` | string | Yes | - | Interval like chr5A:587000000..587200000 |
| `table` | string, default: Genefunc_table | No | Genefunc_table | Genefunc_table or Genefunc_IWGSC03G_table |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/genes/functions/interval?ID=chr5A:587000000..587200000"
```

---


### GET /api/genes/known/search

**Tags:** Genes

**Search Known Genes**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `searchid` | string | Yes | - |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/genes/known/search?searchid=VRN1"
```

---

### GET /api/genes/known/{gene_id}

**Tags:** Genes

**Get Known Gene**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gene_id` | string | Yes | - |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/genes/known/TraesCS5A02G391700"
```

---

### GET /api/health

**Health**

**Example:**
```bash
curl -X GET "http://localhost:8000/api/health"
```

---

### GET /api/homologs/wheat-rice-arabidopsis

**Tags:** Comparative

**Wheat Rice Arabidopsis Homologs**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gene_id` | string | Yes | - |  |
| `max_targets` | integer, default: 3 | No | 3 |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/homologs/wheat-rice-arabidopsis?gene_id=TraesCS5A02G391700&max_targets=3"
```

---

### GET /api/id-conversion

**Tags:** Comparative

**Convert Gene Ids**

Convert external gene IDs to IWGSC v1.1 (02G) format.
Input transcript IDs must include the `.1` suffix, separated by %0D%0A (URL-encoded newline).

Available source databases (`gene_version`):
- `MIPS_result` — MIPSv2.2, e.g. `Traes_1AS_E6058767A.1`
- `TGACv1_result` — TGACv1, e.g. `TRIAE_CS42_6BL_TGACv1_501926_AA1621570.1`
- `IWGSCv1_result` — IWGSCv1.0, e.g. `TraesCS6B01G342500.1`

Response fields: `query_gene` (input), `reference_gene` (IWGSCv1.1), `code` (mapping class), `length`, `not_found`.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ID` | string | Yes | - | Gene IDs with .1 suffix; multiple IDs separated by %0D%0A |
| `gene_version` | string | Yes | - | Source table: MIPS_result / TGACv1_result / IWGSCv1_result |

**Example:**
```bash
# MIPS v2.2 -> IWGSC v1.1 (02G)
curl -X GET "https://wheatomics.sdau.edu.cn/api/id-conversion?ID=Traes_1AS_E6058767A.1&gene_version=MIPS_result"

# TGACv1 -> IWGSC v1.1 (02G), multiple genes (newline-separated)
curl -X GET "https://wheatomics.sdau.edu.cn/api/id-conversion?ID=TRIAE_CS42_6BL_TGACv1_501926_AA1621570.1%0D%0ATRIAE_CS42_6BL_TGACv1_123456_AA1620000.1&gene_version=TGACv1_result"

# IWGSCv1.0 -> IWGSC v1.1 (02G)
curl -X GET "http://localhost:8000/api/id-conversion?ID=TraesCS6B01G342500.1&gene_version=v2"
```

---

### GET /api/novabrowse

**Tags:** Sequences

**Novabrowse Run**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `chrom` | string | Yes | - |  |
| `start` | integer | Yes | - |  |
| `end` | integer | Yes | - |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/novabrowse?chrom=chr5A&start=587000000&end=588000000"
```




### GET /api/ppi/query

**Tags:** Networks

**Query Ppi**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gene_ids` | string | Yes | - |  |
| `table` | string, default: PPI_result | No | PPI_result |  |
| `min_score` | number, default: 0.5 | No | 0.5 |  |

**Example:**
```bash
# 转录本 ID 需加 .1 后缀，不支持 eggNOG ID
# CF-MS 评分阈值: 0.5（高置信）/ 0.2（中等）/ 0（全部）
curl -X GET "https://wheatomics.sdau.edu.cn/api/ppi/query?gene_ids=TraesCS6D02G084800.1&min_score=0.5"
```

---

### GET /api/sequence/batch

**Tags:** Sequences

**Batch Sequence**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `database` | string | Yes | - |  |
| `ID` | string | Yes | - |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/sequence/batch?ID=TraesCS5A02G391700+TraesCS5A02G391700.1&database=all_gene"
```

---

### GET /api/sequence/by-gene

**Tags:** Sequences

**Sequence By Gene**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gene_id` | string | Yes | - |  |
| `gene_db` | string, default: all_gene | No | all_gene |  |
| `protein_db` | string, default: all_protein | No | all_protein |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/sequence/by-gene?gene_id=TraesCS5A02G391700"
```

---

### GET /api/sequence/by-interval

**Tags:** Sequences

**Sequence By Interval**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `region` | string | Yes | - | Legacy region format |
| `database` | string | Yes | - |  |

**Example:**
```bash
curl -X GET "https://wheatomics.sdau.edu.cn/api/sequence/by-interval?region=chr1A_Fielder:587123000-587124000&database=all_genomes"
```

---

### GET /api/synteny/search

**Tags:** Comparative

**Search Synteny**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ID` | string | Yes | - |  |
| `table` | string, default: CSsymaptbl | No | CSsymaptbl |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/synteny/search?ID=TraesCS5A02G391700"
```

---


### GET /api/PrimerServer2/config

**Get Config Endpoint**

---



### GET /api/PrimerServer2/databases

**Get Databases**

---



### POST /api/PrimerServer2/jobs

**Create Job**

**Request Body:** DesignJobRequest (application/json)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app-type` | string | **Yes** | `"design"` |
| `selectTemplate` | string | **Yes** | 模板数据库名（如 `"primer_Chinese_Spring2.1.genome"`）或 `"custom"` |
| `template-regions` | string | No | 模板区域，每行一个：`TemplateID TargetPos TargetLength [ProductSizeMin] [ProductSizeMax]`。`selectTemplate` 非 custom 时必填 |
| `custom-template-sequences` | string | No | 自定义模板 FASTA 序列。`selectTemplate` 为 custom 时必填 |
| `region_type` | string | No | 区域类型：`SEQUENCE_TARGET`（区域内设计）/ `SEQUENCE_INCLUDED_REGION`（扩增全长）/ `FORCE_END`（强制 3' 端）。默认 `SEQUENCE_TARGET` |
| `product_size_min` | int | No | 最小产物大小 (bp)，默认 100 |
| `product_size_max` | int | No | 最大产物大小 (bp)，默认 1000 |
| `selected-databases` | array | No | 特异性检测的数据库列表，默认 `["primer_Chinese_Spring2.1.genome"]` |
| `size_start` | int | No | 特异性检测最小扩增子大小 (bp)，默认 50 |
| `size_stop` | int | No | 特异性检测最大扩增子大小 (bp)，默认 5000 |
| `PRIMER_NUM_RETURN` | int | No | Primer3 每个位点设计的候选引物对数，默认 30 |
| `PRIMER_MIN_SIZE` | int | No | 最小引物长度 (bp)，默认 18 |
| `PRIMER_OPT_SIZE` | int | No | 最佳引物长度 (bp)，默认 20 |
| `PRIMER_MAX_SIZE` | int | No | 最大引物长度 (bp)，默认 23 |
| `PRIMER_MIN_TM` | float | No | 最小退火温度 (°C)，默认 57 |
| `PRIMER_OPT_TM` | float | No | 最佳退火温度 (°C)，默认 60 |
| `PRIMER_MAX_TM` | float | No | 最大退火温度 (°C)，默认 63 |
| `PRIMER_MIN_GC` | float | No | 最小 GC 含量 (%)，默认 35.0 |
| `PRIMER_MAX_GC` | float | No | 最大 GC 含量 (%)，默认 65.0 |
| `blast_e_value` | int | No | BLAST E-value 阈值，默认 30000 |
| `blast_identity` | int | No | BLAST 比对最低相似度 (%)，默认 60 |
| `blast_word_size` | int | No | BLAST word size，默认 7 |
---



### POST /api/PrimerServer2/jobs/check

**Create Check Job**

**Request Body:** CheckJobRequest (application/json)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `app-type` | string | **Yes** | `"check"` |
| `check-primers` | string | **Yes** | 引物组，每行一个：`PrimerID LeftSeq RightSeq` |
| `selected-databases` | array | No | 特异性检测数据库列表，默认 `["primer_Chinese_Spring2.1.genome"]` |
| `size_start` | int | No | 最小扩增子大小 (bp)，默认 50 |
| `size_stop` | int | No | 最大扩增子大小 (bp)，默认 5000 |
| `blast_e_value` | int | No | BLAST E-value 阈值，默认 30000 |
| `blast_identity` | int | No | BLAST 最低相似度 (%)，默认 60 |
---



### POST /api/PrimerServer2/jobs/cleanup

**Cleanup Jobs**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
---



### GET /api/PrimerServer2/jobs/{job_id}

**Get Job**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | string | Yes |  |
---



### DELETE /api/PrimerServer2/jobs/{job_id}

**Delete Job**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | string | Yes |  |
---



### GET /api/PrimerServer2/jobs/{job_id}/progress

**Get Progress**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | string | Yes |  |
---



### GET /api/PrimerServer2/jobs/{job_id}/result

**Get Result**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | string | Yes |  |
| `job_type` | string | No |  |
---



### GET /api/PrimerServer2/jobs/{job_id}/result-html

**Get Result Html**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | string | Yes |  |
---



### GET /api/PrimerServer2/jobs/{job_id}/specificity/{filename}

**Get Specificity Result**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_id` | string | Yes |  |
| `filename` | string | Yes |  |
---



### GET /api/PrimerServer2/server-info

**Get Server Info**

---


## Schemas

### ExpressionGeneResult

```json
{
  "properties": {
    "gene_id": {
      "type": "string",
      "title": "Gene Id"
    },
    "project": {
      "type": "string",
      "title": "Project"
    },
    "points": {
      "items": {
        "$ref": "#/components/schemas/ExpressionPoint"
      },
      "type": "array",
      "title": "Points"
    }
  },
  "type": "object",
  "required": [
    "gene_id",
    "project",
    "points"
  ],
  "title": "ExpressionGeneResult",
  "description": "Expression result per gene."
}
```

### ExpressionPoint

```json
{
  "properties": {
    "label": {
      "type": "string",
      "title": "Label"
    },
    "value": {
      "type": "number",
      "title": "Value"
    },
    "std": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Std"
    },
    "error_bar": {
      "anyOf": [
        {
          "items": {
            "type": "number"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "Error Bar"
    }
  },
  "type": "object",
  "required": [
    "label",
    "value"
  ],
  "title": "ExpressionPoint",
  "description": "One sample or tissue expression point."
}
```

### ExpressionQueryResponse

```json
{
  "properties": {
    "project": {
      "type": "string",
      "title": "Project"
    },
    "genes_found": {
      "type": "integer",
      "title": "Genes Found"
    },
    "genes_not_found": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Genes Not Found"
    },
    "results": {
      "items": {
        "$ref": "#/components/schemas/ExpressionGeneResult"
      },
      "type": "array",
      "title": "Results"
    }
  },
  "type": "object",
  "required": [
    "project",
    "genes_found",
    "results"
  ],
  "title": "ExpressionQueryResponse",
  "description": "Batch expression query response."
}
```

```

```

### HTTPValidationError

```json
{
  "properties": {
    "detail": {
      "items": {
        "$ref": "#/components/schemas/ValidationError"
      },
      "type": "array",
      "title": "Detail"
    }
  },
  "type": "object",
  "title": "HTTPValidationError"
}
```


### SequenceBundle

```json
{
  "properties": {
    "gene_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Gene Id"
    },
    "genome_sequence": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Genome Sequence"
    },
    "gene_sequence": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Gene Sequence"
    },
    "protein_sequence": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Protein Sequence"
    },
    "additional_sequences": {
      "items": {
        "$ref": "#/components/schemas/SequenceRecord"
      },
      "type": "array",
      "title": "Additional Sequences"
    }
  },
  "type": "object",
  "title": "SequenceBundle",
  "description": "Bundled sequences for a gene or interval."
}
```

### SequenceRecord

```json
{
  "properties": {
    "sequence_id": {
      "type": "string",
      "title": "Sequence Id"
    },
    "fasta": {
      "type": "string",
      "title": "Fasta"
    }
  },
  "type": "object",
  "required": [
    "sequence_id",
    "fasta"
  ],
  "title": "SequenceRecord",
  "description": "Named sequence payload."
}
```

```



### DesignJobRequest

```json
{
  "properties": {
    "size_start": {
      "type": "integer",
      "maximum": 100000.0,
      "minimum": 1.0,
      "title": "Size Start",
      "default": 50
    },
    "size_stop": {
      "type": "integer",
      "maximum": 1000000.0,
      "minimum": 1.0,
      "title": "Size Stop",
      "default": 5000
    },
    "min_Tm_diff": {
      "type": "integer",
      "maximum": 100.0,
      "minimum": 0.0,
      "title": "Min Tm Diff",
      "default": 20
    },
    "retain": {
      "type": "integer",
      "maximum": 1000.0,
      "minimum": 1.0,
      "title": "Retain",
      "default": 10
    },
    "end3_mismatch_threshold": {
      "type": "integer",
      "maximum": 5.0,
      "minimum": 0.0,
      "title": "End3 Mismatch Threshold",
      "default": 5
    },
    "max_report_amplicon": {
      "type": "integer",
      "maximum": 10000.0,
      "minimum": 1.0,
      "title": "Max Report Amplicon",
      "default": 50
    },
    "blast_e_value": {
      "type": "integer",
      "minimum": 1.0,
      "title": "Blast E Value",
      "default": 30000
    },
    "blast_word_size": {
      "type": "integer",
      "maximum": 11.0,
      "minimum": 4.0,
      "title": "Blast Word Size",
      "default": 7
    },
    "blast_identity": {
      "type": "integer",
      "maximum": 100.0,
      "minimum": 0.0,
      "title": "Blast Identity",
      "default": 60
    },
    "blast_max_hsps": {
      "type": "integer",
      "minimum": 1.0,
      "title": "Blast Max Hsps",
      "default": 500
    },
    "conc_primer": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc Primer",
      "default": 100.0
    },
    "conc_dNTPs": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc Dntps",
      "default": 0.2
    },
    "conc_Na": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc Na",
      "default": 0.0
    },
    "conc_K": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc K",
      "default": 50.0
    },
    "conc_Tris": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc Tris",
      "default": 10.0
    },
    "conc_Mg": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc Mg",
      "default": 1.5
    },
    "selected-databases": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Selected-Databases"
    },
    "custom-db-sequences": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Custom-Db-Sequences"
    },
    "app-type": {
      "$ref": "#/components/schemas/JobType"
    },
    "selectTemplate": {
      "type": "string",
      "title": "Selecttemplate"
    },
    "template-regions": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Template-Regions"
    },
    "custom-template-sequences": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Custom-Template-Sequences"
    },
    "region_type": {
      "$ref": "#/components/schemas/RegionType",
      "default": "SEQUENCE_TARGET"
    },
    "product_size_min": {
      "type": "integer",
      "maximum": 50000.0,
      "minimum": 30.0,
      "title": "Product Size Min",
      "default": 100
    },
    "product_size_max": {
      "type": "integer",
      "maximum": 50000.0,
      "minimum": 30.0,
      "title": "Product Size Max",
      "default": 1000
    },
    "PRIMER_MIN_SIZE": {
      "type": "integer",
      "maximum": 35.0,
      "minimum": 1.0,
      "title": "Primer Min Size",
      "default": 18
    },
    "PRIMER_OPT_SIZE": {
      "type": "integer",
      "maximum": 35.0,
      "minimum": 1.0,
      "title": "Primer Opt Size",
      "default": 20
    },
    "PRIMER_MAX_SIZE": {
      "type": "integer",
      "maximum": 35.0,
      "minimum": 1.0,
      "title": "Primer Max Size",
      "default": 23
    },
    "PRIMER_MIN_GC": {
      "type": "number",
      "maximum": 100.0,
      "minimum": 0.0,
      "title": "Primer Min Gc",
      "default": 35.0
    },
    "PRIMER_OPT_GC_PERCENT": {
      "type": "number",
      "maximum": 100.0,
      "minimum": 0.0,
      "title": "Primer Opt Gc Percent",
      "default": 50.0
    },
    "PRIMER_MAX_GC": {
      "type": "number",
      "maximum": 100.0,
      "minimum": 0.0,
      "title": "Primer Max Gc",
      "default": 65.0
    },
    "PRIMER_MIN_TM": {
      "type": "number",
      "maximum": 100.0,
      "minimum": 0.0,
      "title": "Primer Min Tm",
      "default": 57.0
    },
    "PRIMER_OPT_TM": {
      "type": "number",
      "maximum": 100.0,
      "minimum": 0.0,
      "title": "Primer Opt Tm",
      "default": 60.0
    },
    "PRIMER_MAX_TM": {
      "type": "number",
      "maximum": 100.0,
      "minimum": 0.0,
      "title": "Primer Max Tm",
      "default": 63.0
    },
    "PRIMER_PAIR_MAX_DIFF_TM": {
      "type": "number",
      "minimum": 0.0,
      "title": "Primer Pair Max Diff Tm",
      "default": 3.0
    },
    "PRIMER_NUM_RETURN": {
      "type": "integer",
      "maximum": 1000.0,
      "minimum": 1.0,
      "title": "Primer Num Return",
      "default": 30
    },
    "PRIMER_MIN_LEFT_THREE_PRIME_DISTANCE": {
      "type": "integer",
      "maximum": 10.0,
      "minimum": -1.0,
      "title": "Primer Min Left Three Prime Distance",
      "default": 3
    },
    "PRIMER_MIN_RIGHT_THREE_PRIME_DISTANCE": {
      "type": "integer",
      "maximum": 10.0,
      "minimum": -1.0,
      "title": "Primer Min Right Three Prime Distance",
      "default": 3
    },
    "PRIMER_MAX_END_STABILITY": {
      "type": "number",
      "minimum": 0.0,
      "title": "Primer Max End Stability",
      "default": 9.0
    },
    "PRIMER_LOWERCASE_MASKING": {
      "type": "integer",
      "maximum": 1.0,
      "minimum": 0.0,
      "title": "Primer Lowercase Masking",
      "default": 0
    },
    "PRIMER_MAX_SELF_ANY_TH": {
      "type": "number",
      "minimum": 0.0,
      "title": "Primer Max Self Any Th",
      "default": 45.0
    },
    "PRIMER_PAIR_MAX_COMPL_ANY_TH": {
      "type": "number",
      "minimum": 0.0,
      "title": "Primer Pair Max Compl Any Th",
      "default": 45.0
    },
    "PRIMER_MAX_SELF_END_TH": {
      "type": "number",
      "minimum": 0.0,
      "title": "Primer Max Self End Th",
      "default": 35.0
    },
    "PRIMER_PAIR_MAX_COMPL_END_TH": {
      "type": "number",
      "minimum": 0.0,
      "title": "Primer Pair Max Compl End Th",
      "default": 35.0
    },
    "PRIMER_MAX_HAIRPIN_TH": {
      "type": "number",
      "minimum": 0.0,
      "title": "Primer Max Hairpin Th",
      "default": 24.0
    }
  },
  "type": "object",
  "required": [
    "app-type",
    "selectTemplate"
  ],
  "title": "DesignJobRequest"
}
```

### CheckJobRequest

```json
{
  "properties": {
    "size_start": {
      "type": "integer",
      "maximum": 100000.0,
      "minimum": 1.0,
      "title": "Size Start",
      "default": 50
    },
    "size_stop": {
      "type": "integer",
      "maximum": 1000000.0,
      "minimum": 1.0,
      "title": "Size Stop",
      "default": 5000
    },
    "min_Tm_diff": {
      "type": "integer",
      "maximum": 100.0,
      "minimum": 0.0,
      "title": "Min Tm Diff",
      "default": 20
    },
    "retain": {
      "type": "integer",
      "maximum": 1000.0,
      "minimum": 1.0,
      "title": "Retain",
      "default": 10
    },
    "end3_mismatch_threshold": {
      "type": "integer",
      "maximum": 5.0,
      "minimum": 0.0,
      "title": "End3 Mismatch Threshold",
      "default": 5
    },
    "max_report_amplicon": {
      "type": "integer",
      "maximum": 10000.0,
      "minimum": 1.0,
      "title": "Max Report Amplicon",
      "default": 50
    },
    "blast_e_value": {
      "type": "integer",
      "minimum": 1.0,
      "title": "Blast E Value",
      "default": 30000
    },
    "blast_word_size": {
      "type": "integer",
      "maximum": 11.0,
      "minimum": 4.0,
      "title": "Blast Word Size",
      "default": 7
    },
    "blast_identity": {
      "type": "integer",
      "maximum": 100.0,
      "minimum": 0.0,
      "title": "Blast Identity",
      "default": 60
    },
    "blast_max_hsps": {
      "type": "integer",
      "minimum": 1.0,
      "title": "Blast Max Hsps",
      "default": 500
    },
    "conc_primer": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc Primer",
      "default": 100.0
    },
    "conc_dNTPs": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc Dntps",
      "default": 0.2
    },
    "conc_Na": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc Na",
      "default": 0.0
    },
    "conc_K": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc K",
      "default": 50.0
    },
    "conc_Tris": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc Tris",
      "default": 10.0
    },
    "conc_Mg": {
      "type": "number",
      "minimum": 0.0,
      "title": "Conc Mg",
      "default": 1.5
    },
    "selected-databases": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Selected-Databases"
    },
    "custom-db-sequences": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Custom-Db-Sequences"
    },
    "app-type": {
      "$ref": "#/components/schemas/JobType"
    },
    "check-primers": {
      "type": "string",
      "title": "Check-Primers"
    }
  },
  "type": "object",
  "required": [
    "app-type",
    "check-primers"
  ],
  "title": "CheckJobRequest"
}
```

### JobResponse

```json
{
  "properties": {
    "jobId": {
      "type": "string",
      "title": "Jobid"
    },
    "status": {
      "$ref": "#/components/schemas/JobStatus"
    },
    "createdAt": {
      "type": "string",
      "title": "Createdat"
    },
    "message": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Message"
    }
  },
  "type": "object",
  "required": [
    "jobId",
    "status",
    "createdAt"
  ],
  "title": "JobResponse"
}
```

### JobResultResponse

```json
{
  "properties": {
    "jobId": {
      "type": "string",
      "title": "Jobid"
    },
    "jobType": {
      "type": "string",
      "title": "Jobtype"
    },
    "status": {
      "$ref": "#/components/schemas/JobStatus"
    },
    "html": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Html"
    },
    "designPrimers": {
      "anyOf": [
        {
          "items": {
            "$ref": "#/components/schemas/PrimerResult"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "Designprimers"
    },
    "checkResults": {
      "anyOf": [
        {
          "items": {
            "$ref": "#/components/schemas/CheckResult"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "Checkresults"
    },
    "error": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Error"
    }
  },
  "type": "object",
  "required": [
    "jobId",
    "jobType",
    "status"
  ],
  "title": "JobResultResponse"
}
```

### ProgressResponse

```json
{
  "properties": {
    "total": {
      "type": "integer",
      "title": "Total"
    },
    "finished": {
      "type": "integer",
      "title": "Finished"
    },
    "percent": {
      "type": "integer",
      "title": "Percent"
    },
    "stage": {
      "type": "string",
      "title": "Stage"
    }
  },
  "type": "object",
  "required": [
    "total",
    "finished",
    "percent",
    "stage"
  ],
  "title": "ProgressResponse"
}
```

### ServerInfoResponse

```json
{
  "properties": {
    "currentTime": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Currenttime"
    },
    "cpuInfo": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Cpuinfo"
    },
    "memTotal": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Memtotal"
    },
    "memFree": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Memfree"
    },
    "samtoolsVersion": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Samtoolsversion"
    },
    "blastnVersion": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Blastnversion"
    },
    "primer3Version": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Primer3Version"
    }
  },
  "type": "object",
  "title": "ServerInfoResponse"
}
```

### ConfigResponse

```json
{
  "properties": {
    "limitSite": {
      "type": "integer",
      "title": "Limitsite"
    },
    "limitPrimer": {
      "type": "integer",
      "title": "Limitprimer"
    },
    "limitDatabase": {
      "type": "integer",
      "title": "Limitdatabase"
    },
    "useCPU": {
      "type": "integer",
      "title": "Usecpu"
    },
    "showInfo": {
      "type": "boolean",
      "title": "Showinfo"
    },
    "removeTmp": {
      "type": "boolean",
      "title": "Removetmp"
    }
  },
  "type": "object",
  "required": [
    "limitSite",
    "limitPrimer",
    "limitDatabase",
    "useCPU",
    "showInfo",
    "removeTmp"
  ],
  "title": "ConfigResponse"
}
```

### DatabasesResponse

```json
{
  "properties": {
    "groups": {
      "items": {
        "$ref": "#/components/schemas/DatabaseGroup"
      },
      "type": "array",
      "title": "Groups"
    }
  },
  "type": "object",
  "required": [
    "groups"
  ],
  "title": "DatabasesResponse"
}
```

### DatabaseGroup

```json
{
  "properties": {
    "name": {
      "type": "string",
      "title": "Name"
    },
    "databases": {
      "additionalProperties": {
        "type": "string"
      },
      "type": "object",
      "title": "Databases"
    }
  },
  "type": "object",
  "required": [
    "name",
    "databases"
  ],
  "title": "DatabaseGroup"
}
```

### PrimerResult

```json
{
  "properties": {
    "siteId": {
      "type": "string",
      "title": "Siteid"
    },
    "rank": {
      "type": "integer",
      "title": "Rank"
    },
    "leftSeq": {
      "type": "string",
      "title": "Leftseq"
    },
    "rightSeq": {
      "type": "string",
      "title": "Rightseq"
    },
    "productSize": {
      "type": "integer",
      "title": "Productsize"
    },
    "penalty": {
      "type": "number",
      "title": "Penalty"
    },
    "leftTm": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Lefttm"
    },
    "rightTm": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Righttm"
    },
    "leftGc": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Leftgc"
    },
    "rightGc": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Rightgc"
    },
    "leftPos": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Leftpos"
    },
    "rightPos": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Rightpos"
    },
    "leftLen": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "title": "Leftlen"
    },
    "rightLen": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "title": "Rightlen"
    },
    "leftSelfAny": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Leftselfany"
    },
    "rightSelfAny": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Rightselfany"
    },
    "leftSelfEnd": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Leftselfend"
    },
    "rightSelfEnd": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Rightselfend"
    },
    "leftHairpin": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Lefthairpin"
    },
    "rightHairpin": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Righthairpin"
    },
    "leftEndStability": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Leftendstability"
    },
    "rightEndStability": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Rightendstability"
    },
    "pairComplAny": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Paircomplany"
    },
    "pairComplEnd": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "null"
        }
      ],
      "title": "Paircomplend"
    },
    "primer3Rank": {
      "anyOf": [
        {
          "type": "integer"
        },
        {
          "type": "null"
        }
      ],
      "title": "Primer3Rank"
    },
    "databases": {
      "items": {
        "additionalProperties": true,
        "type": "object"
      },
      "type": "array",
      "title": "Databases"
    }
  },
  "type": "object",
  "required": [
    "siteId",
    "rank",
    "leftSeq",
    "rightSeq",
    "productSize",
    "penalty",
    "databases"
  ],
  "title": "PrimerResult"
}
```

### CheckResult

```json
{
  "properties": {
    "siteId": {
      "type": "string",
      "title": "Siteid"
    },
    "rank": {
      "type": "integer",
      "title": "Rank"
    },
    "database": {
      "type": "string",
      "title": "Database"
    },
    "ampliconNumber": {
      "type": "integer",
      "title": "Ampliconnumber"
    },
    "primerSeqs": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Primerseqs"
    }
  },
  "type": "object",
  "required": [
    "siteId",
    "rank",
    "database",
    "ampliconNumber",
    "primerSeqs"
  ],
  "title": "CheckResult"
}
```

### JobStatus

```json
{
  "type": "string",
  "enum": [
    "pending",
    "running",
    "done",
    "error",
    "stopped"
  ],
  "title": "JobStatus"
}
```

### JobType

```json
{
  "type": "string",
  "enum": [
    "design",
    "check"
  ],
  "title": "JobType"
}
```

### RegionType

```json
{
  "type": "string",
  "enum": [
    "SEQUENCE_TARGET",
    "SEQUENCE_INCLUDED_REGION",
    "FORCE_END"
  ],
  "title": "RegionType"
}
```

### ValidationError

```json
{
  "properties": {
    "loc": {
      "items": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "integer"
          }
        ]
      },
      "type": "array",
      "title": "Location"
    },
    "msg": {
      "type": "string",
      "title": "Message"
    },
    "type": {
      "type": "string",
      "title": "Error Type"
    },
    "input": {
      "title": "Input"
    },
    "ctx": {
      "type": "object",
      "title": "Context"
    }
  },
  "type": "object",
  "required": [
    "loc",
    "msg",
    "type"
  ],
  "title": "ValidationError"
}
```
