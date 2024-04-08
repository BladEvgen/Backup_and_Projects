package main

import (
	"database/sql"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

const (
	dbHost     = "localhost"
	dbPort     = 5432
	dbUser     = "admin"
	dbPassword = "AaBbCc5153"
	dbName     = "task_manager"
)

type Task struct {
	ID     int    `json:"id"`
	Title  string `json:"title"`
	Status string `json:"status"`
}

func main() {
	fmt.Println("Start")

	connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		dbHost, dbPort, dbUser, dbPassword, dbName)

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	router := gin.Default()

	router.GET("/tasks", func(c *gin.Context) {
		rows, err := db.Query("SELECT id, title, status FROM tasks")
		if err != nil {
			fmt.Println("Не удалось получить задачи из базы данных.:", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Не удалось получить задачи из базы данных."})
			return
		}
		defer rows.Close()

		var tasks []Task
		for rows.Next() {
			var task Task
			err := rows.Scan(&task.ID, &task.Title, &task.Status)
			if err != nil {
				fmt.Println("Не удалось проверить задачу:", err)
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Fе удалось проверить задачу"})
				return
			}
			tasks = append(tasks, task)
		}
		if err := rows.Err(); err != nil {
			fmt.Println("Ошибка во время итерации строк:", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Ошибка во время итерации строк"})
			return
		}

		c.JSON(http.StatusOK, gin.H{"data": tasks})
	})

	router.GET("/tasks/:id", func(c *gin.Context) {
		id := c.Param("id")
		row := db.QueryRow("SELECT id, title, status FROM tasks WHERE id = $1", id)
		var task Task
		err := row.Scan(&task.ID, &task.Title, &task.Status)
		if err != nil {
			fmt.Println("Не удалось получить задачу из базы данных.:", err)
			c.JSON(http.StatusNotFound, gin.H{"error": "Задача не найдена"})
			return
		}
		c.JSON(http.StatusOK, task)
	})

	router.POST("/tasks", func(c *gin.Context) {
		var task Task
		if err := c.BindJSON(&task); err != nil {
			fmt.Println("Не удалось проанализировать тело запроса.:", err)
			c.JSON(http.StatusBadRequest, gin.H{"error": "Не удалось проанализировать тело запроса."})
			return
		}

		_, err := db.Exec("INSERT INTO tasks (title, status) VALUES ($1, $2)", task.Title, task.Status)
		if err != nil {
			fmt.Println("Ошибка вставки данных:", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Ошибка вставки данных"})
			return
		}

		c.JSON(http.StatusCreated, task)
	})

	router.PUT("/tasks/:id", func(c *gin.Context) {
		id := c.Param("id")
		var task Task
		if err := c.BindJSON(&task); err != nil {
			fmt.Println("Не удалось проанализировать тело запроса. :", err)
			c.JSON(http.StatusBadRequest, gin.H{"error": "Не удалось проанализировать тело запроса."})
			return
		}

		_, err := db.Exec("UPDATE tasks SET title = $1, status = $2 WHERE id = $3", task.Title, task.Status, id)
		if err != nil {
			fmt.Println("Не удалось обновить задачу в базе данных.:", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Не удалось обновить задачу в базе данных."})
			return
		}

		c.JSON(http.StatusOK, task)
	})

	router.DELETE("/tasks/:id", func(c *gin.Context) {
		id := c.Param("id")

		_, err := db.Exec("DELETE FROM tasks WHERE id = $1", id)
		if err != nil {
			fmt.Println("Не удалось удалить задачу из базы данных.:", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Не удалось удалить задачу из базы данных."})
			return
		}

		c.JSON(http.StatusOK, gin.H{"message": "Успешное удаление"})
	})

	router.Run(":8001")
}
