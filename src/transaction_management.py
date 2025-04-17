from concurrent.futures import ThreadPoolExecutor

class ParallelHandler:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=8)
    
    def process_transactions(self, txs):
        futures = [self.executor.submit(validate, tx) for tx in txs]
        return [f.result() for f in futures]
