package handler

import (
	"errors"
	"niki/config"
	"niki/database"
	"niki/model"
	"time"

	"gorm.io/gorm"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt"
	"golang.org/x/crypto/bcrypt"
)


func CheckPasswordHash(password, hash string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
	return err == nil
}

func getUserByUsername(e string) (*model.User, error) {
	db := database.DB
	var user model.User
	if err := db.Where(&model.User{Username: e}).Find(&user).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}
	return &user, nil
}


func Login(c *fiber.Ctx) error {

	user_data := &model.User{}
	err := c.BodyParser(user_data)

	if err != nil {
		return err
	}

	if user_data.Username == "" {
		return c.Status(fiber.StatusBadRequest).SendString("Username is required.")
	}

	if user_data.Password == "" {
		return c.Status(fiber.StatusBadRequest).SendString("Password is required.")
	}

	user, err := getUserByUsername(user_data.Username)

	if !CheckPasswordHash(user.Password, user_data.Password){
		return c.Status(fiber.StatusBadRequest).SendString("Invalid username or password.")
	}
	
	token := jwt.New(jwt.SigningMethodHS256)

	claims := token.Claims.(jwt.MapClaims)
	claims["username"] = user.Username
	claims["user_id"] = user.ID
	claims["exp"] = time.Now().Add(time.Hour * 72).Unix()

	user_token, err := token.SignedString([]byte(config.Config("SECRET")))
	if err != nil {
		return c.SendStatus(fiber.StatusInternalServerError)
	}

	return c.JSON(fiber.Map{"status": "success", "message": "Success login", "token": user_token})

}
