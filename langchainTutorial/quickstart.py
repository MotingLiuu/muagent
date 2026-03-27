import requests
import json

# First API call with reasoning
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "stepfun/step-3.5-flash:free",
    "messages": [
        {
          "role": "user",
          "content": "How many r's are in the word 'strawberry'?"
        }
      ],
    "reasoning": {"enabled": True},
    "provider": {
        "sort": "throughput"
      }
  })
)
print(response.json())

# Extract the assistant message with reasoning_details
response = response.json()
data1 = response
response = response['choices'][0]['message']

# Preserve the assistant message with reasoning_details
messages = [
  {"role": "user", "content": "How many r's are in the word 'strawberry'?"},
  {
    "role": "assistant",
    "content": response.get('content'),
    "reasoning_details": response.get('reasoning_details')  # Pass back unmodified
  },
  {"role": "user", "content": "Are you sure? Think carefully."}
]

# Second API call - model continues reasoning from where it left off
response2 = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
      "Authorization": "Bearer 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",
      "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "stepfun/step-3.5-flash:free",
    "messages": messages,  # Includes preserved reasoning_details
    "reasoning": {"enabled": True},
    "provider": {
        "sort": "throughput"
      }
  })
)
print(response2.json())
data2 = response2.json()

all_responses = [data1, data2]
with open('responses.json', 'w') as f:
    json.dump(all_responses, f, indent=4)