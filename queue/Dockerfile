FROM golang:1.22.0-alpine3.19

WORKDIR /app

# pre-copy/cache go.mod for pre-downloading dependencies and only redownloading them in subsequent builds if they change
COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . .

ENV AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY

RUN go build -v -o /usr/local/bin/queue/common/awsutil ./common/awsutil && \
    go build -v -o /usr/local/bin/queue/common/connection ./common/connection && \
    go build -v -o /usr/local/bin/queue/common/util ./common/util && \
    go build -v -o /usr/local/bin/queue/sqs_consume ./sqs_consume && \
    go build -v -o /usr/local/bin/queue/websocket ./websocket && \
    go build -v -o /usr/local/bin/queue ./main.go

CMD ["/usr/local/bin/queue/main"]