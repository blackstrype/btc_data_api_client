import asyncio
import websockets
import json
import ssl
import certifi
from datetime import datetime
from data_storage import DataStorage, FileStorage

async def stream_btc_with_heartbeat(storage: DataStorage):
    url = "wss://ws-feed.exchange.coinbase.com"
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    # We now subscribe to both 'ticker' and 'heartbeat' channels
    subscribe_message = {
        "type": "subscribe",
        "product_ids": ["BTC-EUR"],
        "channels": ["ticker", "heartbeat"]
    }

    try:
        async with websockets.connect(url, ssl=ssl_context) as websocket:
            print(f"--- Connected to Coinbase at {datetime.now()} ---")
            await websocket.send(json.dumps(subscribe_message))
            
            while True:
                raw_response = await websocket.recv()
                data = json.loads(raw_response)
                
                # Handling different message types
                msg_type = data.get("type")
                
                if msg_type == "ticker":
                    print(f"📈 TRADE: €{data.get('price')} | Vol: {data.get('last_size')}")
                    await storage.save(data)
                
                elif msg_type == "heartbeat":
                    # This tells us the connection is alive even if no trades happen
                    print(f"💓 HEARTBEAT: Seq {data.get('sequence')} at {data.get('time')}")

    except asyncio.CancelledError:
        print("\nStopping the stream...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Connection closed. Au revoir!")

if __name__ == "__main__":
    file_storage = FileStorage("btc_history.jsonl")

    try:
        asyncio.run(stream_btc_with_heartbeat(file_storage))
    except KeyboardInterrupt:
        pass # Clean exit on Ctrl+C
