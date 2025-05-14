# imports necessary files
import os
from api_key import ApiKey as gpt
from groq import Groq   
import pandas as pd

#creates a class. This class is used to create a generative AI search assistant using the Groq API.
class gen_ai_search:
    
    def __init__(self, api_key):
        self.gpt_api_key = api_key  # assign groq api_key
        self.client = Groq(api_key=api_key)  # Initialize Groq client
        self.model = "llama-3.3-70b-versatile"  # Updated model name for Groq
    
    def search(self, query):
        try:
            # For Groq, we use chat completions,
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": query,
                    }
                ],
                model=self.model,
            )
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
    def generate(self, query):
        chat_history = {}
        
        while True:
            # Perform the search operation
            response = self.search(query)
            print(f"\nResponse: {response}\n")
            
            # Store the query and response
            chat_history[query] = response
                
            # Get next query
            next_query = input("\nEnter your next query (or type 'q' to quit): ")
            
            if next_query.lower() == 'q':
                break
                
            query = next_query

        return chat_history

# Create an instance of the gen_ai_search class
search_tool = gen_ai_search(api_key=gpt.api_key)

print("\nWelcome to the Groq Generative AI Search Assistant!\n")
result = search_tool.generate(query=input("Enter your search query: ")) 

print("\nHere are the Complete Chat Transcription:\n")
for query, response in result.items():
    print(f"Query: {query}\nResponse: {response}\n")

    data_frame=pd.DataFrame(list(result.items()), columns=['Query', 'Response'])
    data_frame.to_csv('chat_transcript.csv', index=False)
    data_frame.to_excel('chat_transcript.xlsx', index=False)
    data_frame.to_json('chat_transcript.json', orient='records', lines=True)

    print("\nChat transcript saved to 'chat_transcript.csv'.\n")