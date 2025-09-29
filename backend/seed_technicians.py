from datetime import datetime
from db_connection import get_connection  # now works

# Sample Kenyan technicians data
technicians_data = [
    ("John Mwangi", "plumbing,pipe repair", 4.5, "Nairobi", 5, True, 15.0, 120),
    ("Jane Wambui", "electrical,wiring", 4.7, "Nairobi", 7, True, 20.0, 150),
    ("Ali Hassan", "carpentry,furniture repair", 4.2, "Mombasa", 4, True, 12.0, 80),
    ("Grace Otieno", "painting,wall finishing", 4.3, "Kisumu", 3, True, 10.0, 60),
    ("Peter Njoroge", "roofing,metal work", 4.6, "Nairobi", 8, True, 25.0, 200),
    ("Fatuma Mohamed", "gardening,landscaping", 4.1, "Mombasa", 4, True, 12.0, 90),
    ("Samuel Kimani", "electrical,solar panel installation", 4.8, "Nairobi", 10, True, 30.0, 250),
    ("Alice Kamau", "plumbing,pipe repair", 4.4, "Nakuru", 6, True, 18.0, 130)
]

# Connect to DB
conn = get_connection()
cursor = conn.cursor()

# Insert data
for tech in technicians_data:
    cursor.execute("""
        INSERT INTO technicians 
        (name, skills, avg_rating, location, experience_years, availability, price_rate, job_count, last_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (*tech, datetime.now()))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("Seed data inserted successfully!")
