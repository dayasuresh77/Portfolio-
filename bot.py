# Pulse - Daily Summary Bot
# Fetches: weather (wttr.in) + a quote (zenquotes.io)
# Runs: every day at 8 AM IST via GitHub Actions

import requests
from datetime import date

def get_weather(city="Thiruvananthapuram"):
    """Fetch today's weather as a one-line text summary."""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()  # remove trailing newline
    except Exception as e:
        return f"Weather unavailable ({e})"

def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # ZenQuotes returns a list containing a dict: [{"q": "quote", "a": "author"}]
        quote = data[0]["q"]
        author = data[0]["a"]
        return f'"{quote}" — {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"

def build_summary():
    """Assemble the pieces and write them to a file."""
    today = date.today().strftime("%B %d, %Y")
    weather = get_weather()
    quote = get_quote()
    
    summary_text = f"=== PULSE DAILY SUMMARY ({today}) ===\n\n"
    summary_text += f"📍 Weather: {weather}\n\n"
    summary_text += f"✨ Thought for the Day:\n{quote}\n"
    
    # Save it to a text file artifact
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text)
        
    return summary_text

def run():
    """Orchestrate the bot execution."""
    print("Starting Pulse...")
    summary = build_summary()
    print(summary)
    print("Pulse ran successfully.")

if __name__ == "__main__":
    run()
    
