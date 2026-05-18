## Database Setup
 db name = restaurant_db
 
1. Make sure MongoDB is running locally on port 27017.

2. Open MongoDB Compass and connect to `mongodb://localhost:27017/`

3. Create the collection with validation — open the MongoDB shell in
   Compass and run the content of `db/products_scheme.json`

4. Import the seed data — in the MongoDB shell run:

mongoimport --db restaurant_db --collection products --file db/products_seed.json --jsonArray