package handler

import (
  "niki/model"
  "github.com/gofiber/fiber/v2"
  "github.com/gofiber/fiber/v2/middleware/basicauth"
)


func Login(c *fiber.Ctx) error {
	type LoginInput struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}
	type UserData struct {
		ID       uint   `json:"id"`
		Username string `json:"username"`
		Password string `json:"password"`
	}
	var input LoginInput
	var ud UserData

	
}