package main

import (
	"crypto/rand"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
)

var serverId string

func main() {
	var err error
	serverId, err = generateServerId()
	if err != nil {
		log.Fatalf("Failed to generate serverId with error[%s]", err)
	}
	http.HandleFunc("/serverId", getServerId)
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
	})

	log.Printf("Starting server on 3000 port")

	err = http.ListenAndServe(":3000", nil)
	if errors.Is(err, http.ErrServerClosed) {
		log.Printf("server is closed")
	} else if err != nil {
		log.Printf("error[%s] starting server", err)
		os.Exit(1)
	}
}

func getServerId(writer http.ResponseWriter, request *http.Request) {
	data := map[string]interface{}{
		"serverId": serverId,
	}
	jsonData, _ := json.Marshal(data)
	writer.Header().Set("Content-Type", "application/json")
	_, err := writer.Write(jsonData)
	if err != nil {
		log.Printf("Failed to write json with error[%s]", err)
	}
}

func generateServerId() (string, error) {
	b := make([]byte, 4)
	_, err := rand.Read(b)
	if err != nil {
		return "", err
	}
	return fmt.Sprintf("%x", b), nil
}
