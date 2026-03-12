from abc import ABC, abstractmethod
import json

# The "Contract"
class DataStorage(ABC):
    @abstractmethod
    async def save(self, data: dict):
        pass

class FileStorage(DataStorage):
    def __init__(self, filename="trades.jsonl"):
        self.filename = filename

    async def save(self, data: dict):
        with open(self.filename, "a") as f:
            f.write(json.dumps(data) + "\n")

class DatabaseStorage(DataStorage):
    async def save(self, data: dict):
        # Later, you'd put your SQL or NoSQL logic here
        print(f"DEBUG: Mock saving to DB: {data.get('sequence')}")
