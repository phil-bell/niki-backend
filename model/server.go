package model

import (
	"gorm.io/gorm"
)

type Server struct {
	gorm.Model
	ID       uint   `gorm:"primaryKey"`
	Key      string `json:"key"`
	Names    string `json:"names"`
	User     User   `gorm:"references:UserID"`
}
