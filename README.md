# 🪙 Bitcoin Live Stream & Analysis

This project is a high-frequency data pipeline that streams **BTC-EUR** trades from Coinbase via WebSockets, stores them in a durable format, and provides an analysis tool to calculate session statistics.

### 📂 Project Structure
* `live_btc.py`: The **Producer**. Connects to Coinbase and streams live trade and heartbeat data.
* `data_storage.py`: The **Architecture**. Defines the `DataStorage` interface and `FileStorage` implementation.
* `read_trades.py`: The **Consumer**. Parses the saved data to calculate Min, Max, and Average prices.
* `btc_history.jsonl`: The **Database**. A JSON Lines file where each line is a unique trade event.

---

### 🚀 How to Use

#### 1. Installation
Ensure you have the necessary dependencies installed:
```bash
pip install websockets certifi
```

#### 2. Start the Live Stream
Open your terminal and run the producer. This will start printing live trades and heartbeats to your console while silently saving the trades to the disk.
```bash
python live_btc.py
```
*Note: Press `Ctrl+C` when you've gathered enough data to stop the stream.*

#### 3. Analyze the Captured Data
After you've collected some data, run the consumer to calculate the session statistics.
```bash
python read_trades.py
```
This will output the total number of trades, the price range (Min/Max), and the weighted average price for the session.

---

### 🏛️ Architecture Details
The project follows a decoupled approach using the **Strategy Pattern** for data storage:
* **The Contract (`DataStorage`)**: An abstract base class that defines how data *should* be saved.
* **The Implementation (`FileStorage`)**: A concrete class that saves data to a `.jsonl` file. 
* **Scalability**: Want to save to a database instead? Simply create a `DatabaseStorage` class that inherits from `DataStorage` and swap it in `live_btc.py`.

---

### 📝 Data Format
Data is stored in **JSON Lines (.jsonl)** format. Each line is a valid JSON object, making it memory-efficient to read and perfect for high-frequency streaming applications.


