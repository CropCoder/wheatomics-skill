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

### GET /api/coexpression/network

**Tags:** Networks

**Coexpression Network**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gene_ids` | string | Yes | - |  |
| `database` | string, default: CO_PRJEB25639 | No | CO_PRJEB25639 |  |
| `pcc_threshold` | number, default: 0.8 | No | 0.8 |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/coexpression/network?gene_ids=TraesCS5A02G391700,TraesCS5A02G123456&pcc_threshold=0.9"
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
curl -X GET "http://localhost:8000/api/expression/query?gene_ids=TraesCS5A02G391700,TraesCS5A02G123456&project=PRJEB5314_paired_tbl"
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

### GET /api/genes/functions/search

**Tags:** Genes

**Search Gene Functions**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ID` | string | Yes | - |  |
| `table` | string, default: Genefunc_table | No | Genefunc_table |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/genes/functions/search?ID=TraesCS5A02G391700"
```

---

### POST /api/genes/known

**Tags:** Genes

**Submit Known Gene**

**Request Body (JSON):**
```json
// Schema: GeneSubmissionRequest — see schemas section below
{
  "$ref": "#/components/schemas/GeneSubmissionRequest"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/genes/known" \
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

### PUT /api/genes/known/{clone_id}

**Tags:** Genes

**Update Known Gene**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `clone_id` | integer | Yes | - |  |

**Request Body (JSON):**
```json
// Schema: GeneUpdateRequest — see schemas section below
{
  "$ref": "#/components/schemas/GeneUpdateRequest"
}
```

**Example:**
```bash
curl -X PUT "http://localhost:8000/api/genes/known/1" \
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

### GET /api/homologs/triticeae

**Tags:** Comparative

**Triticeae Homologs**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `gene_id` | string | Yes | - |  |
| `max_targets` | integer, default: 1 | No | 1 |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/homologs/triticeae?gene_id=TraesCS5A02G391700&max_targets=2"
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

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ID` | string | Yes | - |  |
| `gene_version` | string | Yes | - |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/id-conversion?ID=TraesCS5A02G391700+TraesCS5A02G123456&gene_version=v3"
```

---

### GET /api/literature/search

**Tags:** Literature

**Search Literature**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `search` | ? | No | - |  |
| `tag` | ? | No | - |  |
| `limit` | integer, default: 50 | No | 50 |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/literature/search?search=drought+tolerance&limit=10"
```

---

### GET /api/literature/tags

**Tags:** Literature

**Popular Tags**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer, default: 20 | No | 20 |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/literature/tags?limit=10"
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

---

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
curl -X GET "http://localhost:8000/api/ppi/query?gene_ids=TraesCS5A02G391700&min_score=0.7"
```

---

### GET /api/preblast

**Tags:** Sequences

**Get Preblast Result**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ID` | string | Yes | - |  |
| `blastp_species` | string | Yes | - |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/preblast?ID=TraesCS5A02G391700&blastp_species=rice"
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
curl -X GET "http://localhost:8000/api/sequence/batch?ID=TraesCS5A02G391700+TraesCS5A02G123456&database=all_gene"
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
| `region` | string | Yes | - | Legacy format like chr1A:10-100 |
| `database` | string | Yes | - |  |

**Example:**
```bash
curl -X GET "http://localhost:8000/api/sequence/by-interval?region=chr5A:587123000-587124000&database=Chinese_Spring_genome"
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

### POST /api/tasks/primer-design

**Tags:** Tasks

**Design Primers**

**Request Body (JSON):**
```json
// Schema: PrimerDesignRequest — see schemas section below
{
  "$ref": "#/components/schemas/PrimerDesignRequest"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/tasks/primer-design" \
```

---

### POST /api/tasks/synteny-figure

**Tags:** Tasks

**Render Synteny Figure**

**Request Body (JSON):**
```json
// Schema: SyntenyFigureRequest — see schemas section below
{
  "$ref": "#/components/schemas/SyntenyFigureRequest"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/tasks/synteny-figure" \
```

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

### GeneSubmissionRequest

```json
{
  "properties": {
    "gene_id": {
      "type": "string",
      "title": "Gene Id"
    },
    "gene_name": {
      "type": "string",
      "title": "Gene Name"
    },
    "chrom_pos": {
      "type": "string",
      "title": "Chrom Pos"
    },
    "phenotype": {
      "type": "string",
      "title": "Phenotype"
    },
    "gene_species": {
      "type": "string",
      "title": "Gene Species"
    },
    "paper_title": {
      "type": "string",
      "title": "Paper Title"
    },
    "paper_doi": {
      "type": "string",
      "title": "Paper Doi"
    },
    "key_result": {
      "type": "string",
      "title": "Key Result"
    },
    "author": {
      "type": "string",
      "title": "Author"
    },
    "author_mail": {
      "type": "string",
      "format": "email",
      "title": "Author Mail"
    },
    "password": {
      "type": "string",
      "title": "Password"
    }
  },
  "type": "object",
  "required": [
    "gene_id",
    "gene_name",
    "chrom_pos",
    "phenotype",
    "gene_species",
    "paper_title",
    "paper_doi",
    "key_result",
    "author",
    "author_mail",
    "password"
  ],
  "title": "GeneSubmissionRequest",
  "description": "Known gene submission/update payload."
}
```

### GeneUpdateRequest

```json
{
  "properties": {
    "gene_id": {
      "type": "string",
      "title": "Gene Id"
    },
    "gene_name": {
      "type": "string",
      "title": "Gene Name"
    },
    "chrom_pos": {
      "type": "string",
      "title": "Chrom Pos"
    },
    "phenotype": {
      "type": "string",
      "title": "Phenotype"
    },
    "gene_species": {
      "type": "string",
      "title": "Gene Species"
    },
    "paper_title": {
      "type": "string",
      "title": "Paper Title"
    },
    "paper_doi": {
      "type": "string",
      "title": "Paper Doi"
    },
    "key_result": {
      "type": "string",
      "title": "Key Result"
    },
    "author": {
      "type": "string",
      "title": "Author"
    },
    "author_mail": {
      "type": "string",
      "format": "email",
      "title": "Author Mail"
    },
    "password": {
      "type": "string",
      "title": "Password"
    },
    "clone_id": {
      "type": "integer",
      "title": "Clone Id"
    }
  },
  "type": "object",
  "required": [
    "gene_id",
    "gene_name",
    "chrom_pos",
    "phenotype",
    "gene_species",
    "paper_title",
    "paper_doi",
    "key_result",
    "author",
    "author_mail",
    "password",
    "clone_id"
  ],
  "title": "GeneUpdateRequest",
  "description": "Known gene update payload."
}
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

### PrimerDesignRequest

```json
{
  "properties": {
    "querydb": {
      "type": "string",
      "title": "Querydb"
    },
    "ploidy": {
      "type": "string",
      "title": "Ploidy"
    },
    "price": {
      "type": "string",
      "title": "Price"
    },
    "caps": {
      "type": "boolean",
      "title": "Caps",
      "default": true
    },
    "kasp": {
      "type": "boolean",
      "title": "Kasp",
      "default": true
    },
    "tm": {
      "type": "string",
      "title": "Tm"
    },
    "size": {
      "type": "string",
      "title": "Size"
    },
    "pick": {
      "type": "string",
      "title": "Pick"
    },
    "markers": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Markers"
    }
  },
  "type": "object",
  "required": [
    "querydb",
    "ploidy",
    "price",
    "tm",
    "size",
    "pick"
  ],
  "title": "PrimerDesignRequest",
  "description": "Request body for legacy SNP primer workflow."
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

### SyntenyFigureRequest

```json
{
  "properties": {
    "style": {
      "type": "string",
      "title": "Style",
      "default": "line"
    },
    "dpi": {
      "type": "integer",
      "title": "Dpi",
      "default": 300
    },
    "format": {
      "type": "string",
      "title": "Format",
      "default": "pdf"
    },
    "font": {
      "type": "string",
      "title": "Font",
      "default": "Arial"
    },
    "diverge": {
      "type": "string",
      "title": "Diverge",
      "default": "RdYlBu"
    },
    "scalebar": {
      "type": "boolean",
      "title": "Scalebar",
      "default": false
    },
    "shadestyle": {
      "type": "string",
      "title": "Shadestyle",
      "default": "curve"
    },
    "figsize": {
      "type": "string",
      "title": "Figsize",
      "default": "12,8"
    },
    "block": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Block"
    },
    "layout": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Layout"
    },
    "bed": {
      "anyOf": [
        {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        {
          "type": "null"
        }
      ],
      "title": "Bed"
    },
    "use_default_bed": {
      "type": "boolean",
      "title": "Use Default Bed",
      "default": true
    }
  },
  "type": "object",
  "required": [
    "block",
    "layout"
  ],
  "title": "SyntenyFigureRequest",
  "description": "Request body for jcvi synteny rendering."
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
