import argparse
from WebCrawler import WebCrawler
from siteMap import siteMap
from PageParser import PageParser


def display_banner():
    """Prints the SpiderLock title banner to the console."""

    # Color definitions (requires colorama, or use standard ANSI codes)
    try:
        from colorama import Fore, Style
        SPIDER_COLOR = Fore.CYAN
        LOCK_COLOR = Fore.MAGENTA
        RESET = Style.RESET_ALL
    except ImportError:
        # Fallback to standard ANSI codes if colorama is not installed
        SPIDER_COLOR = "\033[96m"  # Light Cyan
        LOCK_COLOR = "\033[95m"  # Magenta
        RESET = "\033[0m"

    # The title art (use raw string to handle backslashes if needed, though not strictly necessary here)
    title_art = f"""
    {SPIDER_COLOR} _________ {RESET}     {LOCK_COLOR}.__    .___ {RESET}          {LOCK_COLOR} .__ {RESET}                {SPIDER_COLOR} __ {RESET}
    {SPIDER_COLOR}╱   _____╱{RESET}_____ {LOCK_COLOR}│__│{RESET} __│ _╱{LOCK_COLOR}___________│  │{RESET}   ____   ____ {SPIDER_COLOR}│  │ __ {RESET}
    {SPIDER_COLOR}╲_____  ╲{RESET}╲____ ╲{LOCK_COLOR}│  │{RESET}╱ __ │╱ __ ╲_  __ ╲{LOCK_COLOR}  │{RESET}  ╱  _ ╲_╱ ___╲{SPIDER_COLOR}│  │╱ ╱{RESET}
    {SPIDER_COLOR}╱        ╲{RESET}__│__>>{LOCK_COLOR}  ╱ ╱_╱ ╲  ___╱│  │ ╲╱  │{RESET}_(  <_> )  ╲___{SPIDER_COLOR}│    < {RESET}
    {SPIDER_COLOR}╱_______  ╱{RESET}  __╱{LOCK_COLOR}│__╲____ │╲___  >__│  │____╱{RESET}╲____╱ ╲___  >{SPIDER_COLOR}__│_ ╲{RESET}
    {SPIDER_COLOR}       ╲╱{RESET}│__│           ╲╱   ╲╱                        ╲╱     ╲╱
        """

    print(title_art)
    print(
        f"{SPIDER_COLOR}                     SpiderLock:{RESET} {LOCK_COLOR}Lock down your crawl data. Unlock site health.{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Crawler")
    parser.add_argument('-b', '--bfs', action='store_true', help="Use BFS crawling strategy")
    parser.add_argument('-d', '--dfs', action='store_true', help="Use DFS crawling strategy")
    parser.add_argument('-w', '--web', type=str, required=True, help="Starting webpage URL")
    parser.add_argument('-s', '--summary', action='store_true', help="Show crawl summary")
    parser.add_argument('--seo', action='store_true', help="Run SEO audit")
    parser.add_argument('-e', '--ext', action='store_true', help="Show external links")
    parser.add_argument('-t', '--top', type=int, default=10, help="Show top N pages by links")
    parser.add_argument('-j', '--json', type=str, help="Save crawl graph to JSON file")
    parser.add_argument('-de', '--depth', type=int, default=2, help="Set max crawl depth")
    parser.add_argument('-q', '--quick', action='store_true', help="Quick crawl (shallow depth, e.g., 1)")

    args = parser.parse_args()
    if args.bfs and args.dfs:
        parser.error("Cannot select both BFS and DFS. Choose only one crawling strategy.")

    strategy = 'bfs' if args.bfs else 'dfs' if args.dfs else 'bfs'  # default to BFS
    start_url = args.web

    max_depth=1 if args.quick else args.depth
    print(f"\nStarting crawl on {start_url}")
    print(f"Strategy: {strategy.upper()} | Max Depth: {max_depth}\n")

    crawler=WebCrawler(start_url=start_url,strategy=strategy,max_depth=max_depth,allowed_domains=None)
    crawler.crawl(start_url)

    sitemap=siteMap(crawler.graph)

    if args.summary:
        sitemap.print_summary()
    if args.seo:
        sitemap.seo_audit()
    if args.ext:
        sitemap.external_links()
    if args.top:
        sitemap.top_pages_by_links(args.top)
    if args.json:
        sitemap.to_json(args.json)


if __name__ == '__main__':
    display_banner()
    main()

