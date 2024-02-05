# ticketmaster-dupe


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
