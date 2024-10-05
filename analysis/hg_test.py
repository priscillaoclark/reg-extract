import transformers
import torch

from huggingface_hub import login
API_KEY = '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'
login(token = API_KEY)

#model_id = "meta-llama/Meta-Llama-3.1-70B"
model_id = "facebook/bart-large-cnn"

pipeline = transformers.pipeline(
    "summarization", model=model_id
)
pipeline("""The Commodity Futures Trading Commission (CFTC or Commission) 
is proposing regulations to ensure clearing member funds and assets 
receive the proper treatment in the event the derivatives clearing 
organization (DCO) enters bankruptcy by requiring, among other things, 
that clearing member funds be segregated from the DCO's own funds and 
held in a depository that acknowledges in writing that the funds belong 
to clearing members, not the DCO. In addition, the Commission is 
proposing to permit DCOs to hold customer and clearing member funds at 
foreign central banks subject to certain requirements. Finally, the 
Commission is proposing to require DCOs to conduct a daily calculation 
and reconciliation of the amount of funds owed to customers and 
clearing members and the amount actually held for customers and 
clearing members.""")
