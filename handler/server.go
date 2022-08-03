package handler

import (
	"niki/database"
	"niki/model"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt"
)

func CreateServer(c *fiber.Ctx) error {
	type NewServer struct {
		Key   string     `json:"key"`
		Names string     `json:"names"`
		User  model.User `gorm:"references:UserID"`
	}

	db := database.DB
	server := new(model.Server)
	if err := c.BodyParser(server); err != nil {
		return c.Status(400).JSON(fiber.Map{"status": "error", "message": "Review your input", "data": err})
	}

	id := c.Params("id")
	token := c.Locals("user").(*jwt.Token)

	if !validToken(token, id) {
		return c.Status(500).JSON(fiber.Map{"status": "error", "message": "Invalid token id", "data": nil})
	}

	if err := db.Create(&server).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"status": "error", "message": "Couldn't create server", "data": err})
	}

	key := string(make([]byte, 64))
	server.Key = key

	newServer := NewServer{
		Names: server.Names,
		User:  server.User,
		Key:   server.Key,
	}

	return c.JSON(fiber.Map{"status": "success", "message": "Created server", "data": newServer})
}
