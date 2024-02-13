FROM golang:1.22.0-alpine3.8

WORKDIR /app

COPY . .

RUN go mod download

RUN go build -o queue

CMD ["queue"]