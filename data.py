RESERVATIONS = {
    "SKY001": {"name": "Neir Gandhi", "flight": "SW101", "seat": "14A", "class": "Economy", "status": "confirmed"},
    "SKY002": {"name": "Anish Patel", "flight": "SW205", "seat": "3B", "class": "Business", "status": "confirmed"},
    "SKY003": {"name": "Sara Lee", "flight": "SW101", "seat": "22C", "class": "Economy", "status": "confirmed"},
    "SKY004": {"name": "James Wong", "flight": "SW310", "seat": "8D", "class": "Economy", "status": "confirmed"},
}

FLIGHTS = {
    "SW101": {"route": "New York → Los Angeles", "departure": "Today 9:00 AM", "status": "cancelled"},
    "SW205": {"route": "New York → Chicago", "departure": "Today 11:30 AM", "status": "on time"},
    "SW310": {"route": "New York → Miami", "departure": "Today 2:00 PM", "status": "on time"},
}

ALTERNATIVE_FLIGHTS = {
    "SW101": [
        {"flight": "SW103", "route": "New York → Los Angeles", "departure": "Today 1:00 PM", "seats": "aisle available", "stops": "nonstop", "day": "today"},
        {"flight": "SW105", "route": "New York → Los Angeles", "departure": "Today 5:30 PM", "seats": "middle only", "stops": "1 stop", "day": "today"},
        {"flight": "SW107", "route": "New York → Los Angeles", "departure": "Tomorrow 2:00 AM", "seats": "aisle available", "stops": "nonstop", "day": "tomorrow"},
        {"flight": "SW109", "route": "New York → Los Angeles", "departure": "Tomorrow 10:00 AM", "seats": "aisle available", "stops": "nonstop", "day": "tomorrow"},
    ]
}

CUSTOMER_PREFERENCES = {
    "SKY001": {
        "seat_preference": "aisle",
        "flight_preference": "nonstop",
        "avoids": "red-eye flights (departures between 10pm and 5am)",
        "notes": "Frequent flyer. Prefers morning or afternoon departures."
    },
    "SKY002": {
        "seat_preference": "window",
        "flight_preference": "nonstop",
        "avoids": "early morning flights before 7am",
        "notes": "Business class traveller. Values punctuality."
    },
    "SKY003": {
        "seat_preference": "aisle",
        "flight_preference": "any",
        "avoids": "nothing specific",
        "notes": "Budget conscious. Prefers cheaper options."
    },
}
