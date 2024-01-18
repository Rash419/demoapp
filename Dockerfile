FROM golang:1.21 as build

WORKDIR /app

COPY go.mod ./
COPY go.sum ./

RUN go mod download

COPY main.go main.go

RUN CGO_ENABLED=0 GOOS=linux go build -a -o /demoapp

EXPOSE 3000

CMD [ "/demoapp" ]
