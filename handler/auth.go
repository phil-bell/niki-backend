package handler

import (
	"errors"
	"niki/database"
	"niki/model"
	"time"
	"gorm.io/gorm"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v4"
	"golang.org/x/crypto/bcrypt"
)


func CheckPasswordHash(hash string, password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
	return err == nil
}

func getUserByUsername(username string) (*model.User, error) {
	db := database.DB
	var user model.User
	if err := db.Where(&model.User{Username: username}).Find(&user).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return &user, nil
}


func Login(context *fiber.Ctx) error {

	user_data := &model.User{}
	err := context.BodyParser(user_data)

	if err != nil {
		return err
	}

	if user_data.Username == "" {
		return context.Status(fiber.StatusBadRequest).JSON(fiber.Map{"status": "error", "message": "Username is required."})
	}

	if user_data.Password == "" {
		return context.Status(fiber.StatusBadRequest).JSON(fiber.Map{"status": "error", "message": "Password is required."})
	}

	user, err := getUserByUsername(user_data.Username)
	if !CheckPasswordHash(user.Password, user_data.Password){
		return context.Status(fiber.StatusBadRequest).JSON(fiber.Map{"status": "error", "message": "Invalid username or password."})
	}
	
	claims := jwt.MapClaims{
		"username":  user.Username,
		"user_id": user.ID,
		"exp":   time.Now().Add(time.Hour * 72).Unix(),
	}
	println(claims)
	// Create token
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	println(token)

	// Generate encoded token and send it as response.
	user_token, err := token.SignedString([]byte("secret"))
	println(user_token)
	if err != nil {
		return context.JSON(fiber.Map{"status": "error", "message": fiber.StatusInternalServerError})
	}


	return context.JSON(fiber.Map{"status": "success", "message": "Success login", "token": user_token})

}
