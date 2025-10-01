from collections import deque
class CrawlQueue:
    def __init__(self,strategy='bfs'):
        self.strategy=strategy
        if strategy=='bfs':
            self.container=deque()
        elif self.strategy == 'dfs':
            self.container=[]
        else:
            raise ValueError("Unsupported strategy. Choose 'bfs' or 'dfs'.")

        self.seen_urls = set()
    def push(self,url_and_depth):
        url, _ = url_and_depth
        if url not in self.seen_urls:
            self.container.append(url_and_depth)
            self.seen_urls.add(url)
            return True
        return False

    def pop(self):
        if self.is_empty():
            return None
        if self.strategy=='bfs':
            return self.container.popleft()
        else:
            return self.container.pop()

    def is_empty(self):
        return len(self.container)==0

    def __len__(self):
        return len(self.container)


