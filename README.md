# Animal Rescue Dashboard

### Overview
An interactive Python-based dashboard for Grazioso Salvare animal shelter that enables efficient searching, filtering, and management of rescue animal data using MongoDB. The dashboard provides real-time data visualization and optimized query performance for managing large datasets of rescue animals.

### Features
- **MongoDB Integration**: Efficient NoSQL database queries and data retrieval
- **Interactive Dashboard**: User-friendly web interface for searching and filtering animals
- **Advanced Filtering**: Search by multiple animal characteristics and rescue categories
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Query Optimization**: Optimized MongoDB queries for handling large datasets
- **Data Visualization**: Clear presentation and organization of animal rescue data
- **Real-time Updates**: Dynamic dashboard updates based on user selections

### Technologies Used
- **Language**: Python
- **Database**: MongoDB
- **Libraries**: 
  - PyMongo (MongoDB driver)
  - Dash/Plotly (Dashboard framework)
  - Pandas (Data manipulation)
- **Query Language**: MongoDB Query Language (MQL)

### Project Structure
- `Original/` - Initial version with basic CRUD operations
- `Revised/` - Optimized version with improved queries and UI


### Key Enhancements
The enhanced version includes:
- **Optimized MongoDB Queries**: Improved query performance for faster data retrieval
- **Enhanced Indexing Strategy**: Strategic indexing for better search performance
- **Improved User Interface**: More intuitive dashboard layout and navigation
- **Better Error Handling**: Robust input validation and error messages
- **Efficient Filtering**: Streamlined filtering based on animal categories and characteristics
- **Dashboard Reorganization**: Improved data organization and user experience
- **Code Modularity**: Separated CRUD operations into reusable AnimalShelter class

### Database Schema

#### Animal Collection Structure
```javascript
{
  _id: ObjectId,
  name: String,
  animal_type: String,
  breed: String,
  age_upon_outcome: String,
  color: String,
  sex_upon_outcome: String,
  date_of_birth: Date,
  outcome_type: String,
  location: {
    lat: Number,
    long: Number
  },
  rescue_type: String
}
```

### CRUD Operations

#### AnimalShelter Class Methods

**Create (Insert)**
```python
def create(self, data):
    # Inserts a new animal document into the collection
    # Returns True on success, False on failure
```

**Read (Query)**
```python
def read(self, query):
    # Retrieves animal documents matching the query
    # Returns list of matching documents
```

**Update**
```python
def update(self, query, update_data):
    # Updates animal document(s) matching the query
    # Returns count of modified documents
```

**Delete**
```python
def delete(self, query):
    # Deletes animal document(s) matching the query
    # Returns count of deleted documents
```

### Installation and Setup

#### Prerequisites
- Python 3.x
- MongoDB
- Required Python packages

#### Installation Steps
1. Clone this repository
   ```bash
   git clone https://github.com/ChristinaJimenez32/Animal-Rescue.git
   
   ```

2. Install dependencies
   ```bash
   pip install pymongo
   pip install dash
   pip install plotly
   pip install pandas
   ```

3. Set up MongoDB connection
   - Update database credentials in the configuration file
   - Ensure MongoDB is running locally or connection string is correct

4. Run the application
   ```bash
   python dashboard.py
   ```

###Usage

#### Running the Dashboard
1. Start the application
2. Access the dashboard through your web browser (typically `http://localhost:8050`)
3. Use the interface to:
   - View all rescue animals
   - Filter by rescue type (Water Rescue, Mountain/Wilderness Rescue, Disaster Rescue, etc.) 
   - Search for specific animals by breed, age, or other characteristics
   - View detailed information for each animal
   - Update or delete animal records as needed



#### Data Display
- Interactive table with sortable columns
- Geolocation map for animal locations
- Filtered results based on rescue type selection
- Detailed animal information cards

#### User Interface
- Dropdown menus for rescue type selection
- Search functionality for specific attributes
- Clear and reset options
- Responsive design for different screen sizes

#### Dashboard Examples
<img width="1440" height="900" alt="Screenshot 2025-12-01 at 12 10 52 AM" src="https://github.com/user-attachments/assets/a69e0b32-9c22-4472-b837-61297e696611" />
<img width="1440" height="900" alt="Screenshot 2025-12-01 at 12 10 17 AM" src="https://github.com/user-attachments/assets/c8499ffe-578e-4b40-8fe1-d8ac12dfecd0" />
<img width="1440" height="900" alt="Screenshot 2025-12-01 at 12 10 10 AM" src="https://github.com/user-attachments/assets/bc99ee4d-164c-452d-948d-d6838744989c" />
<img width="1440" height="900" alt="Screenshot 2025-12-01 at 12 09 38 AM" src="https://github.com/user-attachments/assets/3418f2c7-bca0-4aae-8c9f-91cedba2341c" />


### Author
Christina Jimenez

