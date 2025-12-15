"""
Sample Animal Shelter Data 

"""

from pymongo import MongoClient
import random
from datetime import datetime, timedelta

# ============= CONFIGURATION =============
# Change these if needed
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DATABASE_NAME = 'AAC'
COLLECTION_NAME = 'animals'
NUMBER_OF_ANIMALS = 1000
# =========================================

# Connect to local MongoDB
try:
    client = MongoClient(f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}/')
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print(f"Connected to MongoDB at {MONGODB_HOST}:{MONGODB_PORT}")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    print("\nMake sure MongoDB is running:")
    print("  Windows: net start MongoDB")
    print("  macOS: brew services start mongodb-community@7.0")
    print("  Linux: sudo systemctl start mongod")
    exit(1)

# Sample data templates
DOG_BREEDS = [
    'Labrador Retriever Mix', 'German Shepherd', 'Golden Retriever',
    'Chesapeake Bay Retriever', 'Newfoundland', 'Alaskan Malamute',
    'Old English Sheepdog', 'Siberian Husky', 'Rottweiler',
    'Doberman Pinscher', 'Bloodhound', 'Beagle Mix', 'Pit Bull Mix',
    'Australian Shepherd', 'Border Collie', 'Boxer Mix', 'Poodle Mix',
    'Corgi Mix', 'Dachshund', 'Great Dane', 'Mastiff', 'Bulldog',
    'Chihuahua Mix', 'Shih Tzu', 'Yorkshire Terrier', 'Cocker Spaniel'
]

CAT_BREEDS = [
    'Domestic Shorthair Mix', 'Domestic Longhair Mix', 'Siamese Mix',
    'Maine Coon Mix', 'Persian Mix', 'Tabby', 'Calico', 'Tuxedo',
    'Russian Blue Mix', 'Bengal Mix', 'Ragdoll Mix', 'Sphynx Mix'
]

COLORS = [
    'Black', 'Brown', 'White', 'Golden', 'Tan', 'Gray', 
    'Black/White', 'Brown/White', 'Tan/White', 'Tri-color',
    'Blue', 'Red', 'Orange', 'Cream', 'Silver', 'Chocolate',
    'Brindle', 'Merle', 'Sable', 'Fawn'
]

NAMES = [
    'Max', 'Bella', 'Charlie', 'Lucy', 'Cooper', 'Daisy', 'Rocky', 'Luna',
    'Buddy', 'Molly', 'Jack', 'Sadie', 'Duke', 'Sophie', 'Bear', 'Maggie',
    'Oliver', 'Chloe', 'Tucker', 'Lily', 'Toby', 'Zoe', 'Bailey', 'Penny',
    'Rex', 'Ruby', 'Gus', 'Stella', 'Zeus', 'Rosie', 'Louie', 'Lola',
    'Sam', 'Gracie', 'Oscar', 'Emma', 'Bentley', 'Coco', 'Milo', 'Nala',
    'Jake', 'Abby', 'Finn', 'Princess', 'Rusty', 'Ginger', 'Shadow', 'Misty',
    'Bruno', 'Annie', 'Diesel', 'Honey', 'Tank', 'Athena', 'Ace', 'Ellie'
]

RESCUE_TYPES = ['Water', 'Mountain', 'Disaster', None, None]  
SEX_TYPES = ['Intact Male', 'Intact Female', 'Neutered Male', 'Spayed Female']
OUTCOME_TYPES = ['Adoption', 'Transfer', 'Return to Owner', 'Foster']

# Austin, TX area coordinates
BASE_LAT, BASE_LON = 30.2672, -97.7431

def random_nearby_coords():
    """Generate random coordinates near Austin, TX"""
    # Spread animals across 50 mile radius
    lat_offset = random.uniform(-0.7, 0.7)
    lon_offset = random.uniform(-0.7, 0.7)
    return round(BASE_LAT + lat_offset, 4), round(BASE_LON + lon_offset, 4)

def generate_animal_document(animal_id):
    """Generate a single realistic animal document"""
    
    # 70% dogs, 30% cats
    animal_type = 'Dog' if random.random() < 0.7 else 'Cat'
    
    # Select breed
    if animal_type == 'Dog':
        breed = random.choice(DOG_BREEDS)
    else:
        breed = random.choice(CAT_BREEDS)
    
    # Basic info
    name = random.choice(NAMES)
    color = random.choice(COLORS)
    
    # Age: 8 weeks to 10 years
    age_weights = [3, 3, 2, 2, 1, 1, 1, 1]  # More younger animals 
    age_range = random.choices(
        [(8, 52), (52, 104), (104, 156), (208, 260), 
         (260, 312), (312, 364), (364, 416), (416, 520)],
        weights=age_weights
    )[0]
    age_weeks = random.randint(age_range[0], age_range[1])
    
    # Sex
    sex = random.choice(SEX_TYPES)
    
    # Rescue type 
    if animal_type == 'Dog' and random.random() < 0.3:  # 30% of dogs
        rescue_type = random.choice(['Water', 'Mountain', 'Disaster'])
    else:
        rescue_type = None
    
    # Location
    lat, lon = random_nearby_coords()
    
    # Dates
    days_ago = random.randint(0, 365)
    outcome_date = datetime.now() - timedelta(days=days_ago)
    birth_date = outcome_date - timedelta(weeks=age_weeks)
    
    # Outcome
    outcome_type = random.choice(OUTCOME_TYPES)
    outcome_subtype = ''
    if outcome_type == 'Transfer':
        outcome_subtype = random.choice(['Partner', 'Rescue Partner'])
    elif outcome_type == 'Foster':
        outcome_subtype = 'Foster'
    
    # Build document
    document = {
        'animal_id': f'A{animal_id:06d}',
        'animal_type': animal_type,
        'breed': breed,
        'name': name,
        'color': color,
        'age_upon_outcome_in_weeks': age_weeks,
        'sex_upon_outcome': sex,
        'outcome_type': outcome_type,
        'outcome_subtype': outcome_subtype,
        'date_of_birth': birth_date.strftime('%Y-%m-%d'),
        'outcome_date': outcome_date.strftime('%Y-%m-%d'),
        'location_lat': lat,
        'location_long': lon,
    }
    
    # Add rescue type if applicable
    if rescue_type:
        document['rescue_type'] = rescue_type
    
    return document

def create_sample_database(num_animals=1000, clear_existing=True):
    """Create sample database with specified number of animals"""
    
    print("\n" + "="*60)
    print(f"  Grazioso Salvare - Creating Database")
    print("="*60)
    
    # Clear existing data 
    if clear_existing:
        existing_count = collection.count_documents({})
        if existing_count > 0:
            response = input(f"\nFound {existing_count} existing animals. Delete? (y/n): ")
            if response.lower() == 'y':
                collection.delete_many({})
                print(f"Deleted {existing_count} existing records")
            else:
                print("Keeping existing data, adding new animals")
    
    print(f"\nGenerating {num_animals} animals...")
    
    # Generate animals
    animals = []
    batch_size = 100
    
    for i in range(1, num_animals + 1):
        animals.append(generate_animal_document(i))
        
        # Insert in batches
        if i % batch_size == 0:
            collection.insert_many(animals)
            print(f"   Inserted {i}/{num_animals}")
            animals = []
    
    # Insert remaining
    if animals:
        collection.insert_many(animals)
        print(f"   Inserted {num_animals}/{num_animals}")
    
    # Calculate and display stats
    print("\n" + "="*60)
    print("  Database Summary")
    print("="*60)
    
    total = collection.count_documents({})
    dogs = collection.count_documents({'animal_type': 'Dog'})
    cats = collection.count_documents({'animal_type': 'Cat'})
    water_rescue = collection.count_documents({'rescue_type': 'Water'})
    mountain_rescue = collection.count_documents({'rescue_type': 'Mountain'})
    disaster_rescue = collection.count_documents({'rescue_type': 'Disaster'})
    
    print(f"\nTotal: {total} animals")
    print(f"  Dogs: {dogs} ({dogs/total*100:.1f}%)")
    print(f"  Cats: {cats} ({cats/total*100:.1f}%)")
    
    print(f"\nRescue Dogs:")
    print(f"  Water: {water_rescue}")
    print(f"  Mountain: {mountain_rescue}")
    print(f"  Disaster: {disaster_rescue}")
    
    # One sample animal
    sample = collection.find_one()
    if sample:
        print(f"\nSample Animal:")
        print(f"  Name: {sample['name']}")
        print(f"  Type: {sample['animal_type']}")
        print(f"  Breed: {sample['breed']}")
        print(f"  Age: {sample['age_upon_outcome_in_weeks']} weeks")
        if 'rescue_type' in sample:
            print(f"  Rescue: {sample['rescue_type']}")
    
    print("\n" + "="*60)
    print("Database created successfully!")
    print(f"  MongoDB: mongodb://{MONGODB_HOST}:{MONGODB_PORT}")
    print(f"  Database: {DATABASE_NAME}")
    print(f"  Collection: {COLLECTION_NAME}")
    print("="*60 + "\n")

if __name__ == '__main__':
    print("\nGrazioso Salvare - Rescue Animal Database Generator")
    
    try:
        # Create the sample database
        create_sample_database(NUMBER_OF_ANIMALS)
        
        print("SUCCESS! Sample database created.\n")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nPlease check that:")
        print("  1. MongoDB is running")
        print("  2. You have pymongo installed: pip3 install pymongo")
        print("  3. MongoDB is accessible at the configured host/port\n")
    
    finally:
        client.close()