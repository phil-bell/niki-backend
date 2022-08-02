# syntax=docker/dockerfile:1

FROM golang:alpine

WORKDIR /app

RUN go install github.com/cosmtrek/air@latest

COPY go.mod /app
COPY go.sum /app
RUN go mod download

COPY .env ./.env
COPY main.go ./
COPy config ./config
COPY database ./database
COPY handler ./handler
COPY middleware ./middleware
COPY model ./model
COPY router ./router

RUN go build -o /niki

EXPOSE 8080

CMD ["/niki"]