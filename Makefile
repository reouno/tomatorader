.PHONY: graph
graph:
	pydeps tmtrader \
		--reverse --max-bacon 2 \
		--cluster \
		--max-cluster-size 1000 \
		--min-cluster-size 2 \
		--keep-target-cluster \
		--rmprefix tmtrader.