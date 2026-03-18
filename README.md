# 🪙 Bitcoin Live Stream & Analysis

This project is a high-frequency data pipeline that streams **BTC-EUR** trades from Coinbase via WebSockets, stores them in a durable format, and provides an analysis tool to calculate session statistics.

### 📂 Project Structure
* `live_btc.py`: The **Producer**. Connects to Coinbase and streams live trade and heartbeat data.
* `data_storage.py`: The **Architecture**. Defines the `DataStorage` interface and `FileStorage` implementation.
* `read_trades.py`: The **Consumer**. Parses the saved data to calculate Min, Max, and Average prices.
* `btc_history.jsonl`: The **Database**. A JSON Lines file where each line is a unique trade event.
* `artemis_stomp_producer.py`: The **Artemis Messaging Client**. A STOMP-based producer for sending trade data to an ActiveMQ Artemis message broker.
* `artemis_server_setup.sh`: The **Infrastructure Script**. Automates the provisioning of a Hetzner Cloud server from a pre-configured Artemis snapshot.

---

### 🚀 How to Use

#### 1. Installation
Ensure you have the necessary dependencies installed:
```bash
pip install -r requirements.txt
```

#### 2. Deploying the Artemis Server
If you need to spin up a messaging broker, use the provided infrastructure script. This script leverages the **Hetzner Cloud (hcloud) CLI** to create a server from a specific snapshot (`artemis-1`).
```bash
./artemis_server_setup.sh
```
**Note:** The snapshot is pre-configured to automatically start the Artemis broker on system boot. Once the server is online, it will be ready to accept STOMP connections.

#### 3. Start the Live Stream
Open your terminal and run the producer. This will start printing live trades and heartbeats to your console while silently saving the trades to the disk.
```bash
python live_btc.py
```
*Note: Press `Ctrl+C` when you've gathered enough data to stop the stream.*

#### 4. Analyze the Captured Data
After you've collected some data, run the consumer to calculate the session statistics.
```bash
python read_trades.py
```
This will output the total number of trades, the price range (Min/Max), and the weighted average price for the session.

---

### 📡 Messaging & Configuration
The `artemis_stomp_producer.py` script allows the pipeline to broadcast trades to an **ActiveMQ Artemis** broker via the **STOMP** protocol. 

To configure the connection, set the following environment variables (e.g., in a `.env` file):
* `ARTEMIS_HOST`: Server IP/Hostname.
* `ARTEMIS_PORT`: STOMP port (default: 61613).
* `ARTEMIS_USER`: Broker username.
* `ARTEMIS_PASSWORD`: Broker password.

---

### 🏛️ Architecture Details
The project follows a decoupled approach using the **Strategy Pattern** for data storage:
* **The Contract (`DataStorage`)**: An abstract base class that defines how data *should* be saved.
* **The Implementation (`FileStorage`)**: A concrete class that saves data to a `.jsonl` file. 
* **Scalability**: Want to save to a database instead? Simply create a `DatabaseStorage` class that inherits from `DataStorage` and swap it in `live_btc.py`.

---

### 📝 Data Format
Data is stored in **JSON Lines (.jsonl)** format. Each line is a valid JSON object, making it memory-efficient to read and perfect for high-frequency streaming applications.


