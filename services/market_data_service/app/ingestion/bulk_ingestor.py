class BulkIngestor:

    def __init__(self, provider, mapper):
        # Creates the bulk ingestor with the provider used to retrieve data
        # and the mapper used to convert provider data into InvestIQ's format.
        # provider comes from app.providers.yahoo.client.
        # mapper comes from app.providers.yahoo.mapper.
        self.provider = provider
        self.mapper = mapper

    def fetch(self, symbols, period="5d", interval="1h"):
        # Retrieves market data from the provider and passes the raw result
        # through the mapper before returning it to the ingestion pipeline.
        # symbols, period, and interval come from BatchManager.
        # provider.get_market_data() retrieves the raw provider data.
        # mapper.map_market_data() converts that data into InvestIQ's format.
        if not symbols:
            raise ValueError("At least one symbol is required.")

        raw_data = self.provider.get_market_data(
            symbols=symbols,
            period=period,
            interval=interval,
        )

        return self.mapper.map_market_data(
        raw_data,
        interval,
        )