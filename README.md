```
━┏┓━━━━━━━┏┓━━━━━━━┏┓━┏┓━━━━━━━━━━━━━━━┏┓━
┏┛┗┓━━━━━━┃┃━━━━━━┏┛┗┓┃┃━━━━━━━━━━━━━━┏┛┗┓
┗┓┏┛┏┓┏━━┓┃┃┏┓┏━━┓┗┓┏┛┃┗━┓┏━━┓┏━━┓┏━━┓┗┓┏┛
━┃┃━┣┫┃┏━┛┃┗┛┛┃┏┓┃━┃┃━┃┏┓┃┃┏┓┃┃┏┓┃┃━━┫━┃┃━
━┃┗┓┃┃┃┗━┓┃┏┓┓┃┃━┫━┃┗┓┃┗┛┃┃┗┛┃┃┗┛┃┣━━┃━┃┗┓
━┗━┛┗┛┗━━┛┗┛┗┛┗━━┛━┗━┛┗━━┛┗━━┛┗━━┛┗━━┛━┗━┛
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```


Microservices:
![image](https://github.com/bchewy/ticketboost/assets/16286067/09a270e6-46e4-4fab-8ffa-41c702c3ae09)



### Docker Compose
To set up this repository, run `docker-compose up` in the current working directory `.`


### port numbers
- 3p_gateway: 8100
- api_gateway: 8200
- billing: 8002
- database: 8003
- event_crud: 8004
- event_orcha: 8005 
- logging: 8006
- merch_crud: 8007
- merchcart_orcha: 8008
- merchcheckout_orcha: 8009
- notification: 8010
- queue: 8011
- rfid: 8012
- rfid_link: 8013
- seat_crud: 8014
- user_crud: 8015
- venue_crud: 8016
- wallet: 8017


# Others
## Setting up hot reload
This allows the changes you make in your local code to be immediately reflected in the containerized app. Add the following flag to your `docker run` command.<br><br>
`-v <path-to-directory-with-code>:/app`<br><br>
(replace the path with `$(pwd)` for Mac/Linux or `${PWD}` for Windows if your current directory contains the code)

## docker compose tests
Should you not want to test end-to-end docker compose, you can use docker-compose-test.yml, or a different name file.. use `docker compose --file docker-compose-test.yml up --build` to run this, and similarly, `docker compose down` to clean it up.

## docker compose, building with env file
`docker-compose --env-file .env up --build -d` - to build with .env

## Redis Setup: 
`docker run --name redis-ticket-holder -p 6379:6379 -d redis`

## PostgresSQL Setup:
### Setting up the postgres container
`docker run --name esd-postgres -e POSTGRES_PASSWORD=testpassword -d postgres`
### Accesing the postgres container
`docker exec -it esd-postgres psql -U postgres`


venv for python:
activating:
`source venv/bin/activate`
