# syntax=docker/dockerfile:1

FROM goland:latest-alpine

WORKDIR /niki/

COPY go.mod .
COPY go.sum .
RUN go mod download

COPY . .