## Objective
You are working as an engineer for IMDb, the world's most popular and authoritative source for movie, TV, and celebrity content.
Your objective is to build a feature that allows the content team to upload movie-related data using a CSV file, and to provide the necessary APIs to consume this data.

### Functional
1. Users should be able to upload CSV files (format of CSV attached below)
    * Max CSV size can be 100 MB    
2. Users should be able to view the list of all movies/shows available in the system in a paginated manner with necessary filtering and sorting options
    * Pagination
    * Filtering by: year of release , language
    * Sorting by: release_date , ratings 


## Solution and Thought Process
One of the major decisions perhaps the most important one, for this project is to decide a database since we are developing a data store which allows users to upload data via csv files and retrieve data in paginated manner, allowing user to filter by `year of release`, `language` and sort by `release date` and `ratings`.

We need to optimse this system for faster reads and writes. I think we should have some fault tolerance mechanism to handle data loss while processing large csv files, maybe using a message queue before pushing to the db.

Since the data is structured mostly be it movies, shows or artists (future scope) so this encourages to use SQL databases.
If we are worried potential schema design changes then we can consider using nosql database like MongoDB.

I'm more inclined towards using SQL databases due to following reasons : 
* Structured data
* I've prior experience, since I need to complete this assignment in given time frame so I don't want to experiment much.
* We can use message queue for fault tolerance during write operations/csv processing
* For faster reads SQL databases offer indexes
* To further optimse reads we can introduce cache layer 

For scope of this project sticking with SQLite, while both MySQL & PostgreSQL are go to options when it comes to production. So if we have time then will migrate the db to PostgreSQL. SQLite is lightweight and ideal for rapid development.