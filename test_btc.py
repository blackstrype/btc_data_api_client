import unittest
import json
import os
import asyncio
import io
from contextlib import redirect_stdout
from unittest.mock import AsyncMock, patch

# Import the code to test
from live_btc import stream_btc_with_heartbeat
from read_trades import analyze_trades
from data_storage import FileStorage

class TestBTCSystem(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.test_filename = "test_history_temp.jsonl"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_analyze_trades_with_data(self):
        """Verifies that analyze_trades correctly calculates stats from a file."""
        # Setup: Create a temporary JSONL file with known data
        data = [
            {"price": "50000.00", "last_size": "0.1", "type": "ticker"},
            {"price": "51000.00", "last_size": "0.2", "type": "ticker"},
            {"price": "49000.00", "last_size": "0.3", "type": "ticker"},
        ]
        with open(self.test_filename, "w") as f:
            for item in data:
                f.write(json.dumps(item) + "\n")

        # Run the function and capture output
        f = io.StringIO()
        with redirect_stdout(f):
            analyze_trades(self.test_filename)
        output = f.getvalue()

        # Assertions
        self.assertIn("Total Trades Captured: 3", output)
        self.assertIn("Minimum Price:  €49,000.00", output)
        self.assertIn("Maximum Price:  €51,000.00", output)
        self.assertIn("SESSION AVERAGE: €50,000.00", output)

    def test_analyze_trades_empty_file(self):
        """Verifies that analyze_trades handles empty files gracefully."""
        open(self.test_filename, "w").close()
        f = io.StringIO()
        with redirect_stdout(f):
            analyze_trades(self.test_filename)
        output = f.getvalue()
        self.assertIn("No trade data found in the file.", output)

    def test_analyze_trades_no_file(self):
        """Verifies that analyze_trades handles missing files gracefully."""
        f = io.StringIO()
        with redirect_stdout(f):
            analyze_trades("non_existent_file.jsonl")
        output = f.getvalue()
        self.assertIn("Error: non_existent_file.jsonl not found", output)

    async def test_stream_btc_with_heartbeat(self):
        """Verifies that stream_btc_with_heartbeat connects and saves ticker data."""
        # Mock Storage
        mock_storage = AsyncMock()
        
        # Mock WebSocket
        mock_websocket = AsyncMock()
        
        # Simulate receiving a ticker and a heartbeat
        ticker_msg = json.dumps({
            "type": "ticker",
            "price": "50000.00",
            "last_size": "0.1",
            "product_id": "BTC-EUR"
        })
        heartbeat_msg = json.dumps({
            "type": "heartbeat",
            "sequence": 12345,
            "time": "2023-10-27T10:00:00Z"
        })
        
        # Return ticker, then heartbeat, then raise CancelledError to stop the loop
        mock_websocket.recv.side_effect = [ticker_msg, heartbeat_msg, asyncio.CancelledError()]

        # Mock websockets.connect to return our mock_websocket (as context manager)
        with patch("websockets.connect") as mock_connect:
            # mock_connect(url, ...) returns a context manager
            mock_connect.return_value.__aenter__.return_value = mock_websocket
            
            # Since stream_btc_with_heartbeat will catch the CancelledError, it won't raise it back to us
            f = io.StringIO()
            with redirect_stdout(f):
                await stream_btc_with_heartbeat(mock_storage)
            output = f.getvalue()
        
        # Verify ticker was saved
        mock_storage.save.assert_called_once()
        saved_data = mock_storage.save.call_args[0][0]
        self.assertEqual(saved_data["type"], "ticker")
        self.assertEqual(saved_data["price"], "50000.00")
        
        # Verify heartbeat was processed but not saved
        self.assertIn("💓 HEARTBEAT", output)
        self.assertIn("Stopping the stream...", output)

    async def test_file_storage(self):
        """Verifies that FileStorage correctly saves data to a file."""
        storage = FileStorage(self.test_filename)
        data = {"price": "50000.00", "last_size": "0.1", "type": "ticker"}
        
        await storage.save(data)
        
        with open(self.test_filename, "r") as f:
            lines = f.readlines()
        
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0]), data)

if __name__ == "__main__":
    unittest.main()
