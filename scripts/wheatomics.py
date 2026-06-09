#!/usr/bin/env python3
"""WheatOmics API client - query the wheat multi-omics database from CLI.

Usage:
  python3 wheatomics.py <endpoint> [key=value ...] [--data @file.json]
  python3 wheatomics.py --list

Examples:
  # Gene detail
  python3 wheatomics.py genes/detail/TraesCS5A02G391700

  # Coexpression query with params
  python3 wheatomics.py coexpression/query gene_ids=TraesCS5A02G391700,TraesCS5B02G123400 database=wheat_expv1 filter_value=0.8

  # Expression query
  python3 wheatomics.py expression/query gene_ids=TraesCS5A02G391700 project=wheat_expression_public_TPM_v1

  # POST with JSON body
  python3 wheatomics.py tasks/primer-design --data @payload.json

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
        ("GET", "genes/functions/search", "Search gene functions (interval/gene/PFAM)"),
        ("GET", "genes/known/search", "Search known genes"),
        ("GET", "genes/known/{gene_id}", "Get known gene detail"),
        ("POST", "genes/known", "Submit known gene"),
        ("PUT", "genes/known/{clone_id}", "Update known gene"),
    ],
    "Expression": [
        ("GET", "expression/projects", "List expression projects"),
        ("GET", "expression/query", "Query expression values"),
    ],
    "Networks": [
        ("GET", "coexpression/databases", "List coexpression databases"),
        ("GET", "coexpression/query", "Query coexpression pairs"),
        ("GET", "coexpression/network", "Build coexpression network graph"),
        ("GET", "ppi/query", "Query PPI interactions"),
    ],
    "Sequences": [
        ("GET", "sequence/by-gene", "Get CDS+protein FASTA by gene"),
        ("GET", "sequence/batch", "Batch FASTA (space-separated IDs)"),
        ("GET", "sequence/by-interval", "Genomic DNA by interval (max 5Mb)"),
        ("GET", "preblast", "Precomputed BLAST results"),
        ("GET", "novabrowse", "Novabrowse genome browser"),
    ],
    "Comparative": [
        ("GET", "homologs/triticeae", "Triticeae homologs"),
        ("GET", "homologs/wheat-rice-arabidopsis", "Wheat-rice-Arabidopsis orthologs"),
        ("GET", "id-conversion", "Convert gene ID versions"),
        ("GET", "synteny/search", "Search syntenic blocks"),
    ],
    "Literature": [
        ("GET", "literature/search", "Search literature"),
        ("GET", "literature/tags", "Popular literature tags"),
    ],
    "Tasks": [
        ("POST", "tasks/primer-design", "Design SNP primers (CAPS/KASP)"),
        ("POST", "tasks/synteny-figure", "Render synteny figure"),
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

    if params:
        query_string = urllib.parse.urlencode(params)
        url = f"{url}?{query_string}"

    req = urllib.request.Request(url, method=method)
    req.add_header("Accept", "application/json")

    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        req.add_header("Content-Type", "application/json")
        req.add_header("Content-Length", str(len(data)))
    else:
        data = None

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
