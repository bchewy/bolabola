# TicketBoost


Microservices:
![image](https://github.com/bchewy/ticketboost/assets/16286067/09a270e6-46e4-4fab-8ffa-41c702c3ae09)



### Docker Compose
To set up this repositoriy, run `docker-compose up` in the current working directory `.`




# Others
Redis Setup: 
`docker run --name redis-ticket-holder -p 6379:6379 -d redis`

PostgresSQL Setup:
### Setting up the postgres container
`docker run --name esd-postgres -e POSTGRES_PASSWORD=testpassword -d postgres`
### Accesing the postgres container
`docker exec -it esd-postgres psql -U postgres`


venv for python:
activating:
`source venv/bin/activate`
