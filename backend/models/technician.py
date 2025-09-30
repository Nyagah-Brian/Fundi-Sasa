# backend/models/technician.py

class Technician:
    def __init__(self, row):
        self.id = row.get("id")
        self.name = row.get("name")
        self.skills = row.get("skills")
        self.location = row.get("location")
        self.price_rate = row.get("price_rate")
        self.experience_years = row.get("experience_years")
        self.avg_rating = row.get("avg_rating")
        self.job_count = row.get("job_count")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "skills": self.skills,
            "location": self.location,
            "price_rate": self.price_rate,
            "experience_years": self.experience_years,
            "avg_rating": self.avg_rating,
            "job_count": self.job_count
        }
