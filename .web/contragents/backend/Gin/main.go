package main

import (
	"database/sql"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

type LogData struct {
	IP         string `json:"ip"`
	Timestamp  int64  `json:"timestamp"`
	StatusCode int    `json:"status_code"`
	Method     string `json:"method"`
	Path       string `json:"path"`
	UserAgent  string `json:"user_agent"`
	Message    string `json:"message"`
	Username   string `json:"username"`
}

const (
	dbHost     = "localhost"
	dbPort     = 5432
	dbUser     = "admin"
	dbPassword = "admin"
	dbName     = "django_log"
)

func insertLogData(data LogData) error {
	connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		dbHost, dbPort, dbUser, dbPassword, dbName)

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return fmt.Errorf("failed to connect to database: %v", err)
	}
	defer db.Close()

	if _, err := db.Exec(`CREATE TABLE IF NOT EXISTS logs (
		id SERIAL PRIMARY KEY,
		ip VARCHAR(45),
		timestamp BIGINT,
		status_code SMALLINT,
		method VARCHAR(10),
		path VARCHAR(255),
		user_agent TEXT,
		message VARCHAR(255),
		username VARCHAR(100)
	)`); err != nil {
		return fmt.Errorf("failed to create table: %v", err)
	}

	_, err = db.Exec(`INSERT INTO logs (ip, timestamp, status_code, method, path, user_agent, message, username)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
		data.IP, data.Timestamp, data.StatusCode, data.Method, data.Path, data.UserAgent, data.Message, data.Username)
	if err != nil {
		return fmt.Errorf("failed to insert data into table: %v", err)
	}

	return nil
}

func main() {
	router := gin.Default()

	router.POST("/api/logs", func(c *gin.Context) {
		var data LogData
		if err := c.BindJSON(&data); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON format"})
			return
		}

		if err := insertLogData(data); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusOK, gin.H{"message": "Log data inserted successfully"})
	})

	router.Run("0.0.0.0:8001")
}
