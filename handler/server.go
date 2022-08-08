package handler

import (
	"niki/database"
	"niki/model"
	"fmt"
	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt"
	"github.com/google/uuid"

)

func CreateServer(context *fiber.Ctx) error {
	type NewServer struct {
		Name 			string `json:"name"`
		UserRefer int    `json:user_id`
	}

	db := database.DB
	server := new(model.Server)

	if err := context.BodyParser(server); err != nil {
		return context.Status(400).JSON(fiber.Map{"status": "error", "message": "Review your input", "data": err})
	}

	var user model.User
	db.Find(&user, server.UserRefer)
	server.User = user

	key := uuid.New()
	server.Key = key.String()

	return context.JSON(fiber.Map{"status": "success", "message": "Created server", "data": server})

	token := context.Locals("user").(*jwt.Token)

	if !validToken(token, "1") {
		return context.Status(500).JSON(fiber.Map{"status": "error", "message": "Invalid token id", "data": nil})
	}

	if err := db.Create(&server).Error; err != nil {
		return context.Status(500).JSON(fiber.Map{"status": "error", "message": "Couldn't create server", "data": err})
	}

	return context.JSON(fiber.Map{"status": "success", "message": "Created server", "data": server})
}


// func GetServer(context *fiber.Ctx) error {
// 	id := context.Params("id")
// 	db := database.DB
// 	var server model.Server
// 	db.Find(&server, id)
// 	if server.Name == "" {
// 		return context.Status(404).JSON(fiber.Map{"status": "error", "message": "No server found with ID", "data": nil})
// 	}
// 	return context.JSON(fiber.Map{"status": "success", "message": "server found", "data": server})
// }