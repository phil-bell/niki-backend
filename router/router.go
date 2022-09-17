package router

import (
	"niki/handler"
	jwtware "github.com/gofiber/jwt/v3"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"
)

// SetupRoutes setup router api
func SetupRoutes(app *fiber.App) {
	api := app.Group("/api", logger.New())
	api.Get("/", handler.Hello)
	
	// Auth
	auth := api.Group("/auth")
	auth.Post("/login", handler.Login)

	// Middleware
	app.Use(jwtware.New(jwtware.Config{
		SigningKey: []byte("secret"),
	}))


	// User
	user := api.Group("/user")
	user.Get("/:id", handler.GetUser)
	user.Post("/", handler.CreateUser)

	// Server
	server := api.Group("/server")
	// server.Get("/:id", handler.GetServer)
	// server.Get("/", handler.ListServer)
	server.Post("/", handler.CreateServer)
}
