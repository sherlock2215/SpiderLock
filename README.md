# Spiderlock

![Logo](images/SpiderLock.png) 

**Spiderlock** is a Python web crawler designed for cybersecurity enthusiasts, pentesters, and web analysts. It supports both **breadth-first (BFS)** and **depth-first (DFS)** crawling strategies and can visualize website structures as a **2D graph**, showing pages and their connections.

---

## Badges

![Python](https://img.shields.io/badge/python-3.11-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![Issues](https://img.shields.io/github/issues/sherlock2215/SpiderLock)

---

## Features

- **BFS & DFS crawling** – Choose the strategy based on your analysis needs.
- **Robots.txt aware** – Automatically respects crawling rules.
- **Sitemap generation** – Builds a clear map of website pages and their links.
- **Export to JSON** – Save crawl graph and results in JSON format.
- **External links handling** – Show and analyze external links.
- **SEO audit** – Optional SEO analysis of pages.
- **Customizable depth & delay** – Control crawl depth and request delay.
- **Modular & Pythonic** – Easy to extend or integrate into pentesting workflows.

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sherlock2215/SpiderLock.git
cd SpiderLock
```

2. Install dependencies (preferably in a virtual environment):
```bash
pip install -r requirements.txt
```

---

## Usage

Run the crawler from the command line:

```bash
python crawler.py -w https://example.com [options]
```

### Available Options
 -----------------------------------------------------------------
| Flag               | Description                                |
|--------------------|--------------------------------------------|
| `-b, --bfs`        | Use BFS crawling strategy                  |
| `-d, --dfs`        | Use DFS crawling strategy                  |
| `-w, --web`        | **Required**. Starting webpage URL         |
| `-s, --summary`    | Show crawl summary                         |
| `    --seo`        | Run SEO audit                              |
| `-e, --ext`        | Show external links                        |
| `-t, --top N`      | Show top N pages by links (default 10)     |
| `-j, --json FILE`  | Save crawl graph to JSON file              |
| `-de,--depth N`    | Set max crawl depth (default 2)            |
| `-q, --quick`      | Quick crawl (shallow depth, e.g., depth 1) |
 -----------------------------------------------------------------
### Example Commands

- **Basic BFS crawl with summary**:
```bash
python crawler.py -w https://example.com -b -s
```

- **DFS crawl, export to JSON, and show external links**:
```bash
python crawler.py -w https://example.com -d -j output.json -e
```

- **Quick crawl with top 5 pages**:
```bash
python crawler.py -w https://example.com -b -q -t 5
```

---

## Example Output

```
Starting crawl on https://example.com
Strategy: BFS | Max Depth: 1

Visited Pages:
[0] https://example.com
[1] https://www.iana.org/domains/example

Crawl complete. Total pages visited: 2
```

The **2D graph visualization** shows pages as nodes and links as edges.

---

## Screenshots / Demo

![Demo](images/quick_crawl.png) 

---

## Future Features

- Multi-threaded crawling for speed
- Browser simulation (JavaScript support)

---

## Contributing

Contributions are welcome! Please open an issue or pull request for bug fixes, features, or improvements.
