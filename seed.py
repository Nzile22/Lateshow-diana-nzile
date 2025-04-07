from app import create_app, db
from models import Episode, Guest, Appearance
from faker import Faker

fake = Faker()

app = create_app()

with app.app_context():
    db.create_all()
    
   
    episodes = []
    for _ in range(10):
        episode = Episode(
            date=fake.date(),
            number=fake.random_int(min=1, max=100)
        )
        db.session.add(episode)
        episodes.append(episode)
    
  
    guests = []
    for _ in range(10):
        guest = Guest(
            name=fake.name(),
            occupation=fake.job()
        )
        db.session.add(guest)
        guests.append(guest)
    
    db.session.commit()  
    

    for _ in range(20):
        appearance = Appearance(
            rating=fake.random_int(min=1, max=5),
            episode_id=fake.random_element(elements=[e.id for e in episodes]),
            guest_id=fake.random_element(elements=[g.id for g in guests])
        )
        db.session.add(appearance)
    
    db.session.commit()
    print("Database seeded successfully!")
