import stomp
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

class ArtemisProducer:
    def __init__(self):
        # Get config from environment, providing defaults if missing
        self.host = os.getenv('ARTEMIS_HOST', 'localhost')
        self.port = int(os.getenv('ARTEMIS_PORT', 61613))
        self.user = os.getenv('ARTEMIS_USER', 'admin')
        self.password = os.getenv('ARTEMIS_PASSWORD', 'admin')

        self.conn = stomp.Connection([(self.host, self.port)])
        self.conn.connect(self.user, self.password, wait=True)
        print(f" Successfully connected to {self.host}:{self.port}")

    async def send_trade(self, trade_data):
        """Sinks a single trade event into the trades.btc queue"""
        destination = 'trades.btc'
        headers={'destination-type': 'ANYCAST'}
        body = json.dumps(trade_data)

        self.conn.send(body=body, destination=destination, headers=headers)
        print(f"✉️  Sent trade to ActiveMQ {destination}: {trade_data.get('price')}")

    def close(self):
        self.conn.disconnect()

