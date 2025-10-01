import json
from collections import defaultdict


class siteMap:
    """
    Manages the crawl graph data and provides methods to:
    - Export it to JSON
    - Print a readable summary
    - Show top pages by number of links
    - Highlight external links
    - Run a simple SEO audit
    """

    def __init__(self, crawl_graph):
        self.graph = crawl_graph

    # ---------------- JSON export ----------------
    def to_json(self, filename="crawler_results.json"):
        """Saves the crawl graph dictionary to a JSON file."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.graph, f, indent=4)
            print(f"\nCrawl graph saved to {filename}")
        except Exception as e:
            print(f"\nError saving JSON file: {e}")

    # ---------------- Summary ----------------
    def print_summary(self):
        """Prints a quick summary of the crawl."""
        total_pages = len(self.graph)
        total_http_links = sum(len(v["categorized_links"]["http(s)_links"]) for v in self.graph.values())
        total_mailto = sum(len(v["categorized_links"]["mail_links"]) for v in self.graph.values())
        total_videos = sum(len(v["categorized_links"]["video_links"]) for v in self.graph.values())
        total_images = sum(len(v["categorized_links"]["image_links"]) for v in self.graph.values())

        print("\n===== Crawl Summary =====")
        print(f"Total pages crawled: {total_pages}")
        print(f"Total HTTP(s) links: {total_http_links}")
        print(f"Total mailto links: {total_mailto}")
        print(f"Total video links: {total_videos}")
        print(f"Total image links: {total_images}")
        print("==========================\n")

    # ---------------- Top pages by number of links ----------------
    def top_pages_by_links(self, n=10):
        """Prints the top N pages with the most HTTP links."""
        pages_sorted = sorted(
            self.graph.items(),
            key=lambda x: len(x[1]["categorized_links"]["http(s)_links"]),
            reverse=True
        )
        print(f"Top {n} pages by number of HTTP links:")
        for page, data in pages_sorted[:n]:
            print(f"{page} -> {len(data['categorized_links']['http(s)_links'])} links")
        print("")

    # ---------------- External links ----------------
    def external_links(self):
        """Lists all HTTP(s) links pointing outside the crawled domain."""
        print("\nExternal links found:")
        all_pages = set(self.graph.keys())
        for page, data in self.graph.items():
            for link in data["categorized_links"].get("http(s)_links", []):
                if link not in all_pages:
                    print(f"{page} -> {link}")
        print("")

    # ---------------- Optional colored summary ----------------
    def colored_summary(self):
        """Prints a summary using colored terminal output (requires colorama)."""
        try:
            from colorama import Fore, Style
        except ImportError:
            print("Install colorama for colored output: pip install colorama")
            return self.print_summary()

        print(f"{Fore.GREEN}Total pages crawled: {len(self.graph)}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}HTTP(s) links: {sum(len(v['categorized_links']['http(s)_links']) for v in self.graph.values())}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Mailto links: {sum(len(v['categorized_links']['mail_links']) for v in self.graph.values())}{Style.RESET_ALL}")
        print(f"{Fore.RED}Video links: {sum(len(v['categorized_links']['video_links']) for v in self.graph.values())}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Image links: {sum(len(v['categorized_links']['image_links']) for v in self.graph.values())}{Style.RESET_ALL}\n")

    # ---------------- SEO audit ----------------
    def seo_audit(self):
        try:
            from colorama import Fore, Style
        except ImportError:
            print("Install colorama for colored output: pip install colorama")
            return self.print_summary()

        missing_titles = []
        duplicate_titles = defaultdict(list)
        missing_h1s = []

        titles_seen = {}

        for page, data in self.graph.items():
            title = data["metrics"].get("title", "").strip()
            if not title:
                missing_titles.append(page)
            else:
                normalized_title = title.lower()
                if normalized_title in titles_seen:
                    duplicate_titles[normalized_title].append(page)
                else:
                    titles_seen[normalized_title] = [page]

            h1 = data["metrics"].get("h1", "").strip()
            if not h1:
                missing_h1s.append(page)

        print(f"\n{Fore.CYAN}====== SEO AUDIT REPORT ======{Style.RESET_ALL}")

        if missing_titles:
            print(f"{Fore.RED}Missing Title Tags ({len(missing_titles)} pages):{Style.RESET_ALL}")
            for url in missing_titles:
                print(f"    - {url}")
        else:
            print(f"{Fore.GREEN}All pages have Title Tags.{Style.RESET_ALL}")

        duplicates_to_report = {k: v for k, v in duplicate_titles.items() if len(v) > 1}
        if duplicates_to_report:
            print(f"\n{Fore.YELLOW} Duplicate Title Tags ({len(duplicates_to_report)} unique titles):{Style.RESET_ALL}")
            for title, pages in duplicates_to_report.items():
                print(f"    - Title: '{title}' appears on:")
                for url in pages:
                    print(f"        - {url}")
        else:
            print(f"\n{Fore.GREEN}No duplicate Title Tags found.{Style.RESET_ALL}")

        if missing_h1s:
            print(f"\n{Fore.RED}Missing H1 Tags ({len(missing_h1s)} pages):{Style.RESET_ALL}")
            for url in missing_h1s:
                print(f"    - {url}")
        else:
            print(f"\n{Fore.GREEN}All pages have H1 Tags.{Style.RESET_ALL}")

        print(f"{Fore.CYAN}=============================={Style.RESET_ALL}\n")
