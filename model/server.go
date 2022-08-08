package model

import (
	"gorm.io/gorm"
)

type Server struct {
	gorm.Model
	ID   			uint   `gorm:"primaryKey"`
	Key  			string `json:"key"`
	Name 			string `json:"name"`
	UserRefer int 	 `json:user_id`
	User 			User   `gorm:"references:UserRefer"`
}
