# SkyWave Airlines Customer Service Agent

An AI-powered customer service agent for SkyWave Airlines built with OpenAI GPT-4o and Streamlit.

---

## What It Can Do

- Answer FAQ questions about baggage, check-in, flight changes, seats, loyalty programs, and special assistance
- Look up reservations by booking ID or passenger name
- Check flight status
- Find alternative flights filtered by day
- Recommend flights based on customer preferences (seat type, nonstop, avoids red-eyes)
- Confirm rebooking with newly assigned seat number
- Escalate frustrated customers or unknown questions to a human agent

---

## Tech Stack

- Python 3.11+
- OpenAI GPT-4o — LLM with function calling
- Streamlit — chat UI
- python-dotenv — environment variable management

---

## Project Structure

- app.py — Streamlit UI and agent logic with tools
- data.py — Mock reservations, flights, and customer preferences
- faq.md — SkyWave Airlines FAQ content
- .env.example — Placeholder for environment variables
- requirements.txt — Python dependencies

---

## Getting Started

1. Clone the repo and cd into it
2. Run: pip install -r requirements.txt
3. Copy .env.example to .env and add your OpenAI API key
4. Run: streamlit run app.py
5. Open http://localhost:8501 in your browser

---

## Example Conversations to Try

- "What is the baggage allowance?"
- "My name is Neir Gandhi"
- "Is my flight on time?"
- "I can only fly tomorrow"
- "Book me on the 10am flight, window seat"
- "I've been waiting weeks and I'm really frustrated"

---

## Mock Booking IDs for Testing

- SKY001 — Neir Gandhi — SW101 — New York to Los Angeles (cancelled)
- SKY002 — Anish Patel — SW205 — New York to Chicago
- SKY003 — Sara Lee — SW101 — New York to Los Angeles
- SKY004 — James Wong — SW310 — New York to Miami

Flight SW101 is cancelled to demo the rebooking flow.

---

## Development Approach

This agent was built incrementally:

1. Started with a simple FAQ-answering agent to validate the core conversational experience
2. Added reservation lookup, flight status checks, and rebooking tools
3. Layered in customer preferences to personalize recommendations
4. Fixed seat assignment so rebooking actually reflects new seat preferences

---

## Notes

This is a demo project using mock data. No real airline systems are connected. API keys are never committed to the repo.
