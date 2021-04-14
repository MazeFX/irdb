
# The Internet Rock Database
 
The go to resource on the internet for all rock related information and overall Rock Awesomeness.

Provided by [Rockstars IT](https://www.teamrockstars.nl/)

## Project goals

This project is created for the Tech Screening Exercise for Java from Team Rockstars IT. The main goal will be to
create a web API with CRUD capabilities for all rock related information.

## My interpretation

The functional requirement for loading in data from json files (or json formatted data) is somewhat awkward.
The CRUD requirement already gives the main method of adding data to the storage (database or otherwise) so any other
way to add data should go through the CRUD mechanism. Therefore I decided to focus on a Restful web API with a complete
functional stack.

- Main web API Service

    A Tornado based web server for handling the CRUD requests and propagation to the Database

- Database Backend

    A MongoDB instance for storage of the data. Since I see a lot of potential in this ap it is important to stay
    flexible with the data requirements. It is obvious that the amount and types of data will be expanded on in the
    future. Currently for testing purposes and local development I will create a data seeder which will load 
    the Json file that are provided.
    
    The request that we are only interested in 'Metal' from before 2016 seems out of place. There has been plenty of
    awesome 'Rock' made after 2016 and this seems like a requirement that will be the first to go. For now the seeder
    will filter the data but since this filter should be dynamic in nature (as in user defined per addition) it is not 
    a good solution.

- Docker Compose

    I will use docker-compose to set things u as a service so that it is possible to extend this to kubernetes or other
    container based platform to speed up CI/CD when the time comes.


## Extra Requirements

For the extra requirements I will focus on the following options as these are in my opinion currently the best options
within the 4 hours that is given.

- Tests: We can not do anything without at least unittests so we should start with that. 
- Database: We choose a MongoDB database to store the data
- Docker: We need a mechanism to run the stack and the containers to make the transition to CI/CD and Production
- API Documentation: Documentation will be provided by Swagger, we need to known how this API works in order to use it.


## Things to Note

I have to be honest and say that it has been at least 2 years since I created a Web API myself. My main experience has
been base on software running on embedded hardware and communication through MQTT. I took the liberty to use a little
more time (6,5 hours) to search for the latest ins and outs and also to give a better picture of what my capabilities
are. Just because you can not play the acoustic guitar perfectly does not mean you can't shread it on a Metal Axe :)