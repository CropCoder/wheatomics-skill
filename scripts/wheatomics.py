#!/usr/bin/env python3
"""WheatOmics API client - query the wheat multi-omics database from CLI.

Usage:
  python3 wheatomics.py <endpoint> [key=value ...] [--data @file.json]
  python3 wheatomics.py --list

Examples:
  # 取基因组区间序列（新端点，推荐）
  python3 wheatomics.py sequence/by-interval region=chr1A_Fielder:587123000-587124000 database=all_genomes

  # Coexpression query with params
  python3 wheatomics.py coexpression/query gene_ids=TraesCS5A02G391700,TraesCS5B02G123400 database=CO_PRJEB25639 filter_value=0.8

  # Expression query（仅支持 02G 基因 ID）
  python3 wheatomics.py expression/query gene_ids=TraesCS5A02G391700 project=PRJEB5314_paired_tbl

  # 按基因 ID 取序列
  python3 wheatomics.py sequence/by-gene gene_id=TraesCS7A03G1158600

  # 按蛋白 ID 取序列
  python3 wheatomics.py sequence/by-gene gene_id=TraesCS7A03G1158600 protein_db=all_protein

  # Batch FASTA（空格分隔 ID，带 .1 后缀）
  python3 wheatomics.py sequence/batch 'ID=TraesCS5A02G391700.1 TraesCS5A02G123400.1' database=all_gene



  # BLAST: 查看可用数据库
  python3 wheatomics.py blast/databases

  # BLAST: 蛋白比对
  python3 wheatomics.py blast/search database=Fielder_protein query='>seq\nMSSSTGTPSA...' program=blastp max_target_seqs=5 save_html=true

  # BLAST: 查看服务器状态
  python3 wheatomics.py blast/status

  # 基因详情

  # List all available endpoints
  python3 wheatomics.py --list
"""

import json
import sys
import urllib.request
import urllib.error
import urllib.parse
import os

BASE_URL = "https://wheatomics.sdau.edu.cn/api"

# Known endpoints for --list
ENDPOINTS = {
    "Meta": [
        ("GET", "about", "Get API info"),
        ("GET", "health", "Health check"),
    ],
    "Genes": [
        ("GET", "genes/detail/{gene_id}", "Gene detail (IWGSC v1/v2/v3)"),
        ("GET", "genes/functions/pfam", "PfamSearch: search genes by PFAM domain (PF prefix)"),
        ("GET", "genes/functions/interval", "IntervalTool: search genes by chromosome interval"),
        ("GET", "genes/functions/tables", "List available gene function tables"),
        ("GET", "genes/functions/examples", "List genome examples for Interval Tool"),
        ("GET", "genes/known/search", "Search known genes"),
        ("GET", "genes/known/all", "List all known genes"),
        ("GET", "genes/known/by-chromosome/{chromosome}", "List known genes by chromosome"),
        ("GET", "genes/known/{gene_id}", "Get known gene detail"),
    ],
    "Expression": [
        ("GET", "expression/projects", "List expression projects"),
        ("GET", "expression/query", "Query expression values"),
    ],
    "Networks": [
        ("GET", "coexpression/databases", "List coexpression databases"),
        ("GET", "coexpression/query", "Query coexpression pairs (PCC threshold or Mutual Rank)"),
        ("GET", "ppi/query", "wheatPPI: query protein interactions (CF-MS score, transcript IDs need .1 suffix)"),
    ],
    "Sequences": [
        ("GET", "sequence/by-gene", "Get CDS+protein FASTA by gene"),
        ("GET", "sequence/batch", "Batch FASTA (space-separated IDs)"),
        ("GET", "sequence/by-interval", "基因组区间序列"),
        ("GET", "novabrowse", "Novabrowse genome browser"),
    ],
    "Comparative": [
        ("GET", "homologs/triticeae", "Triticeae homologs"),
        ("GET", "homologs/wheat-rice-arabidopsis", "Wheat-rice-Arabidopsis orthologs"),
        ("GET", "id-conversion", "Convert external gene IDs to IWGSC v1.1 (02G)"),
        ("GET", "synteny/search", "Search syntenic blocks"),
    ],
        "BLAST": [
        ("GET", "blast/databases", "List available BLAST databases"),
        ("GET", "blast/status", "Check BLAST environment status"),
        ("GET", "blast/search", "Submit BLAST search (blastp/blastn)"),
        ("GET", "preblast", "Precomputed BLAST results by species"),
        ("GET", "blastp", "Search precomputed BLASTP results (paginated)"),
    ],

    "Triticeae Papers": [
        ("GET", "triticeae/papers", "Search Triticeae research papers with filters"),
        ("GET", "triticeae/papers/{pubmedid}", "Get paper details by PubMed ID"),
    ],
    "Tasks": [
    ],
    "PrimerServer2": [
        ("GET", "PrimerServer2/databases", "List PCR primer databases"),
        ("GET", "PrimerServer2/config", "Get server config"),
        ("GET", "PrimerServer2/server-info", "Get server info"),
        ("POST", "PrimerServer2/jobs", "Submit PCR design job"),
        ("POST", "PrimerServer2/jobs/check", "Submit specificity check job"),
        ("GET", "PrimerServer2/jobs/{job_id}", "Get job status"),
        ("DELETE", "PrimerServer2/jobs/{job_id}", "Delete job"),
        ("GET", "PrimerServer2/jobs/{job_id}/progress", "Get job progress"),
        ("GET", "PrimerServer2/jobs/{job_id}/result", "Get job result"),
        ("GET", "PrimerServer2/jobs/{job_id}/result-html", "Get HTML result"),
        ("GET", "PrimerServer2/jobs/{job_id}/specificity/{filename}", "Get specificity file"),
        ("POST", "PrimerServer2/jobs/cleanup", "Cleanup old jobs"),
    ],

}


def list_endpoints():
    """Print all available endpoints."""
    for category, eps in ENDPOINTS.items():
        print(f"\n{category}:")
        for method, path, desc in eps:
            print(f"  {method:6s} /api/{path:45s} {desc}")


def parse_args(args):
    """Parse CLI args into endpoint, params dict, and data file."""
    endpoint = None
    params = {}
    data_file = None

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--list":
            list_endpoints()
            sys.exit(0)
        elif arg == "--data":
            i += 1
            if i < len(args):
                data_file = args[i]
            else:
                print("Error: --data requires a file argument (@filename)", file=sys.stderr)
                sys.exit(1)
        elif "=" in arg:
            key, value = arg.split("=", 1)
            params[key] = value
        elif endpoint is None:
            endpoint = arg
        else:
            print(f"Warning: ignoring extra positional arg: {arg}", file=sys.stderr)
        i += 1

    if endpoint is None:
        print("Usage: wheatomics.py <endpoint> [key=value ...] [--data @file.json]", file=sys.stderr)
        print("       wheatomics.py --list", file=sys.stderr)
        sys.exit(1)

    return endpoint, params, data_file


def request(method, path, params=None, json_body=None):
    """Make an API request and return parsed JSON."""
    url = f"{BASE_URL}/{path.lstrip('/')}"

    if method.upper() == "POST" and params and json_body is None:
        # Form-urlencoded POST (e.g., BLAST search)
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    elif json_body is not None:
        # JSON body POST (e.g., PrimerServer2 jobs)
        data = json.dumps(json_body).encode("utf-8")
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
    elif params:
        # GET query params
        query_string = urllib.parse.urlencode(params)
        full_url = f"{url}?{query_string}"
        req = urllib.request.Request(full_url, method=method)
        data = None
    else:
        req = urllib.request.Request(url, method=method)
        data = None
    
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, data=data, timeout=30) as resp:
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read()

            if "application/json" in content_type:
                return json.loads(raw)
            else:
                # FASTA or plain text
                return raw.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        if body:
            try:
                print(json.dumps(json.loads(body), indent=2, ensure_ascii=False), file=sys.stderr)
            except json.JSONDecodeError:
                print(body[:500], file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    endpoint, params, data_file = parse_args(sys.argv[1:])

    # Determine method
    if endpoint.startswith("POST ") or endpoint.startswith("post "):
        method = "POST"
        path = endpoint[5:]
    elif endpoint.startswith("PUT ") or endpoint.startswith("put "):
        method = "PUT"
        path = endpoint[4:]
    elif endpoint.startswith("GET ") or endpoint.startswith("get "):
        method = "GET"
        path = endpoint[4:]
    else:
        method = "GET"
        path = endpoint
        # Detect from known endpoints
        for category, eps in ENDPOINTS.items():
            for ep_method, ep_path, _ in eps:
                if ep_path == path.rstrip('/'):
                    method = ep_method
                    break

    # Parse JSON body if --data provided
    json_body = None
    if data_file:
        if data_file.startswith("@"):
            filepath = data_file[1:]
            if not os.path.exists(filepath):
                print(f"Error: data file not found: {filepath}", file=sys.stderr)
                sys.exit(1)
            with open(filepath) as f:
                json_body = json.load(f)
        else:
            json_body = json.loads(data_file)

    result = request(method, path, params, json_body)

    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
