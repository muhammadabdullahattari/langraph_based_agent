import chromadb

class LongTermMemory:
    def __init__(self,collection_name: str = "agent_memory",persist_directory: str = ".chroma") -> None:
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def store(self,session_id: str,summary: str,) -> None:
        self.collection.add(ids=[session_id],documents=[summary])

    def retrieve(self,query: str,limit: int = 3,) -> list[str]:
        if self.collection.count() == 0:
            return []

        results = self.collection.query(query_texts=[query],n_results=limit,)

        return results.get("documents", [[]])[0]