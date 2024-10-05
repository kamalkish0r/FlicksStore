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

### DB Discussion 
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


### API Design 

1. User should be able to upload files 

    When it comes to large files it's always better to process in chunks to prevent memory overflow leading to server kill.
    One of the popular approach is to do client side handling to directly push the file to a cloud bucket(GCS, S3) and share the pre-signed url with server. This way we don't have to any network handling, all is all handled by the cloud provider. But that will require a bunch of configuration & client side handling so skipping for now.

    We can utilise background processing on the server side to handle processing of large csv files. Once upload is completed, we trigger a background task and immediately return the response to the user with status message along with `task_id` which can be used to fetch the status of the job

2. DB Setup : 

    Now let's setup & initialise DB. For schema I'm thinking of using the csv header as it is. Later might come back and rethink about optimisation.
    
    ~~ToDo : Revisit the DB schema design.~~

    After taking the closer look at the csv, I noticed that a movie can be in multiple languages, then there are multiple entities like Genre, Production Companies etc. so splitting the data accordingly and establishing the relationship via foreign key.
    For now not focusing much on the DB performance, will revisit and optimise it later.

3. Get Data : 

    A controller with all the required filters as query params.
