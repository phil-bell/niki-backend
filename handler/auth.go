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
		return context.Status(fiber.StatusBadRequest).SendString("Username is required.")
	}

	if user_data.Password == "" {
		return context.Status(fiber.StatusBadRequest).SendString("Password is required.")
	}

	user, err := getUserByUsername(user_data.Username)
	if !CheckPasswordHash(user.Password, user_data.Password){
		return context.Status(fiber.StatusBadRequest).SendString("Invalid username or password.")
	}
	
	token := jwt.New(jwt.SigningMethodHS256)

	claims := token.Claims.(jwt.MapClaims)
	claims["username"] = user.Username
	claims["user_id"] = user.ID
	claims["exp"] = time.Now().Add(time.Hour * 72).Unix()

	user_token, err := token.SignedString([]byte(config.Config("SECRET")))
	if err != nil {
		return context.SendStatus(fiber.StatusInternalServerError)
	}

	return context.JSON(fiber.Map{"status": "success", "message": "Success login", "token": user_token})

}
