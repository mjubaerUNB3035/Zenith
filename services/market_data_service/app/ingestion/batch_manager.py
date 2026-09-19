class BatchManager:

    def __init__(self, ingestor, batch_size=100):
        # Creates the batch manager.
        # ingestor is provided by the Market Data Service and should be a BulkIngestor.
        # BatchManager does not know which market-data provider BulkIngestor uses.
        self.ingestor = ingestor
        self.batch_size = batch_size

    def fetch_in_batches(self, symbols, period="5d", interval="1h"):
        # Splits the symbols into batches and asks BulkIngestor to fetch each batch.
        # symbols come from the Market Data Service ingestion request.
        # BulkIngestor comes from app.ingestion.bulk_ingestor.
        # BulkIngestor then communicates with the configured provider.
        if not symbols:
            raise ValueError("At least one symbol is required.")

        results = []

        for i in range(0, len(symbols), self.batch_size):
            batch = symbols[i:i + self.batch_size]

            result = self.ingestor.fetch(
                symbols=batch,
                period=period,
                interval=interval,
            )

            results.append(result)

        return results