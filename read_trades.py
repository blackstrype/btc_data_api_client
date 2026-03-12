import json
import os

def analyze_trades(filename="btc_history.jsonl"):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found. Run your stream script first!")
        return

    prices = []
    
    print(f"--- Analyzing Data from {filename} ---")
    
    with open(filename, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                
                # Extract the price and convert to float for math
                price = float(data.get("price"))
                prices.append(price)
            except (json.JSONDecodeError, ValueError, TypeError):
                # Skip malformed lines or heartbeats if they accidentally got in
                continue

    if not prices:
        print("No trade data found in the file.")
        return

    # Calculate statistics
    avg_price = sum(prices) / len(prices)
    max_price = max(prices)
    min_price = min(prices)
    trade_count = len(prices)

    print(f"Total Trades Captured: {trade_count}")
    print(f"Minimum Price:  €{min_price:,.2f}")
    print(f"Maximum Price:  €{max_price:,.2f}")
    print(f"---")
    print(f"SESSION AVERAGE: €{avg_price:,.2f}")

if __name__ == "__main__":
    analyze_trades()
