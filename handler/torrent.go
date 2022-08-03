package handler

import (
	"niki/database"
	"niki/model"
	"github.com/golang-jwt/jwt"
	"github.com/gofiber/fiber/v2"
)


func CreateTorrent(c *fiber.Ctx) error {
	type NewTorrent struct {
		Location string 	  `json:"location"`
		Magnet   string 	  `json:"magnet"`
		Names    string 	  `json:"names"`
		Server model.Server `gorm:"references:ServerID"`
		User     model.User   `gorm:"references:UserID"`
	}

	db := database.DB
	torrent := new(model.Torrent)
	if err := c.BodyParser(torrent); err != nil {
		return c.Status(400).JSON(fiber.Map{"status": "error", "message": "Review your input", "data": err})
	}

	id := c.Params("id")
	token := c.Locals("user").(*jwt.Token)

	if !validToken(token, id) {
		return c.Status(500).JSON(fiber.Map{"status": "error", "message": "Invalid token id", "data": nil})
	}

	if err := db.Create(&torrent).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"status": "error", "message": "Couldn't create user", "torrent": err})
	}

	newTorrent := NewTorrent{
		Location: torrent.Location,
		Magnet:   torrent.Magnet,
		Names:    torrent.Names,
		Server: 	torrent.Server,
		User:   	torrent.User,
	}

	return c.JSON(fiber.Map{"status": "success", "message": "Created torrent", "data": newTorrent})
}