# syntax=docker/dockerfile:1

FROM golang:alpine

WORKDIR /app

RUN go install github.com/cosmtrek/air@latest

COPY go.mod go.sum /app

RUN go mod download

COPY . /app

RUN go build -o /niki

EXPOSE 3000

CMD ["/niki"]