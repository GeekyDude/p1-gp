import uuid
from google.cloud.firestore_v1 import Increment

def IncrementBy(doc_ref, field, incrementValue):
    shardId = str(uuid.uuid4())
    counter_ref = doc_ref.collection("_counter_shards_").document(shardId)

    counter_ref.set({field : Increment(incrementValue)}, merge=True)

def TransactionIncrement(transaction, doc_ref, field, incrementValue):
    shardId = str(uuid.uuid4())
    counter_ref = doc_ref.collection("_counter_shards_").document(shardId)
    transaction.set(counter_ref, {field : Increment(incrementValue)}, merge=True)