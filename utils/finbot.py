from dotenv import load_dotenv
import cohere
import os

load_dotenv()
api_key = os.getenv('COHERE_API_KEY')
co = cohere.Client(api_key)

def get_budget_insights(user_query, transactions_text):
    prompt = f"""User query: {user_query}\nTransactions list: {transactions_text}\n
    You are FinBot, a financial AI assistant developed by Sakshi & Shahu for the Finfluener budgeting app and Respond to the user in a single, well-structured paragraph, ensuring that all sentences are complete and coherent, without any breaks or cutoff.
    Your job is **ONLY** to assist users with their **financial queries**, including budgeting, expense tracking, and savings advice. **DO NOT** answer anything that is unrelated to finance. If a user asks something outside finance, firmly respond with: 
    "I can only assist with financial-related questions. Please ask me something about your finances."
    If user asks about making changes his expenses or income to delete or add ,simply respond:""I can assist you with managing your finances, but I cannot make changes to your expenses or income. You can update or modify them on the respective pages. Let me know if you'd like help with anything else!"
    If the user asks about **yourself**, simply respond:
    "I am FinBot, a financial assistant built by Sakshi & Shahu to help with budgeting and expense management."""

    response = co.generate(
        model='command-xlarge-nightly',  
        prompt=prompt,
        max_tokens=100
    )
    
    # Return the response from Cohere API
    return response.generations[0].text.strip()