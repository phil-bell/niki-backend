package model

import (
	"time"

	"gorm.io/gorm"
)

type Torrent struct {
	gorm.Model
	ID         uint      `gorm:"primaryKey"`
	Location   string    `json:"location"`
	Magnet     string    `json:"magnet"`
	Names      string    `json:"names"`
	Server 	   Server
	User       User
	CompleteAt time.Time `json:"CompleteAt"`
}
