import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import json
from data import RESERVATIONS, FLIGHTS, ALTERNATIVE_FLIGHTS

load_dotenv()

client = OpenAI()

with open("faq.md", "r") as f:
    faq_content = f.read()

def lookup_reservation(booking_id: str = None, name: str = None) -> str:
    if booking_id:
        booking_id = booking_id.upper()
        res = RESERVATIONS.get(booking_id)
        if res:
            return f"Found reservation {booking_id}: {res['name']}, Flight {res['flight']}, Seat {res['seat']}, Class {res['class']}, Status: {res['status']}."
        return f"No reservation found for booking ID {booking_id}."
    if name:
        name_lower = name.lower()
        for bid, res in RESERVATIONS.items():
            if name_lower in res["name"].lower():
                return f"Found reservation {bid}: {res['name']}, Flight {res['flight']}, Seat {res['seat']}, Class {res['class']}, Status: {res['status']}."
        return f"No reservation found for name {name}."
    return "Please provide a booking ID or name."

def check_flight_status(flight_number: str) -> str:
    flight = FLIGHTS.get(flight_number.upper())
    if flight:
        return f"Flight {flight_number} ({flight['route']}) departing {flight['departure']} is currently {flight['status']}."
    return f"No flight found with number {flight_number}."

def find_alternative_flights(flight_number: str, day: str = None) -> str:
    alternatives = ALTERNATIVE_FLIGHTS.get(flight_number.upper())
    if not alternatives:
        return f"No alternative flights found for {flight_number}."
    if day:
        alternatives = [a for a in alternatives if a.get("day", "").lower() == day.lower()]
    if not alternatives:
        return f"No alternative flights found for {flight_number} on {day}."
    result = f"Alternative flights for {flight_number}:\n"
    for i, alt in enumerate(alternatives, 1):
        result += f"{i}. Flight {alt['flight']} — {alt['route']}, departing {alt['departure']}, {alt['stops']}, seats: {alt['seats']}\n"
    return result

def confirm_rebooking(original_flight: str, new_flight: str, booking_id: str) -> str:
    booking_id = booking_id.upper()
    if booking_id in RESERVATIONS:
        RESERVATIONS[booking_id]["flight"] = new_flight
        new = FLIGHTS.get(new_flight, {})
        return f"Rebooking confirmed. {RESERVATIONS[booking_id]['name']} has been moved from {original_flight} to {new_flight} ({new.get('route', '')}), departing {new.get('departure', '')}."
    return f"Could not confirm rebooking. Reservation {booking_id} not found."

tools = [
    {
        "type": "function",
        "function": {
            "name": "lookup_reservation",
            "description": "Look up a customer reservation by booking ID or passenger name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {"type": "string", "description": "The booking ID e.g. SKY001"},
                    "name": {"type": "string", "description": "The passenger name"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_flight_status",
            "description": "Check whether a flight is on time or cancelled.",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_number": {"type": "string", "description": "The flight number e.g. SW101"}
                },
                "required": ["flight_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_alternative_flights",
            "description": "Find alternative flights when a flight is cancelled or customer wants to reschedule. Filter by day if specified.",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_number": {"type": "string", "description": "The flight number to find alternatives for"},
                    "day": {"type": "string", "description": "Filter by day: 'today' or 'tomorrow'"}
                },
                "required": ["flight_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "confirm_rebooking",
            "description": "Confirm rebooking a passenger from one flight to another.",
            "parameters": {
                "type": "object",
                "properties": {
                    "original_flight": {"type": "string", "description": "The original flight number"},
                    "new_flight": {"type": "string", "description": "The new flight number"},
                    "booking_id": {"type": "string", "description": "The passenger booking ID"}
                },
                "required": ["original_flight", "new_flight", "booking_id"]
            }
        }
    }
]

tool_map = {
    "lookup_reservation": lookup_reservation,
    "check_flight_status": check_flight_status,
    "find_alternative_flights": find_alternative_flights,
    "confirm_rebooking": confirm_rebooking,
}

st.title("SkyWave Airlines Customer Service")
st.caption("Ask me about your booking, flight status, or anything else.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"""You are a helpful customer service agent for SkyWave Airlines.
You can look up reservations by booking ID or passenger name.
You can check flight status, find alternative flights, and confirm rebooking.
When the customer specifies a day (today, tomorrow), always filter alternatives to that day only.
For general questions, use the FAQ below.
If a question is outside the FAQ and you cannot help with tools, say you are escalating to a human agent.
If a customer is frustrated, escalate immediately with empathy.
Always be friendly, concise, and professional.

FAQ:
{faq_content}"""}
    ]

for msg in st.session_state.messages:
    if isinstance(msg, dict) and msg.get("role") in ["user", "assistant"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            while True:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        m if isinstance(m, dict) else m.model_dump()
                        for m in st.session_state.messages
                    ],
                    tools=tools,
                    tool_choice="auto"
                )

                message = response.choices[0].message

                if message.tool_calls:
                    st.session_state.messages.append(message)
                    for tool_call in message.tool_calls:
                        fn_name = tool_call.function.name
                        fn_args = json.loads(tool_call.function.arguments)
                        fn_result = tool_map[fn_name](**fn_args)
                        st.session_state.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": fn_result
                        })
                else:
                    reply = message.content
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.write(reply)
                    break
