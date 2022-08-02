package model

import "gorm.io/gorm"

// User struct
type User struct {
	gorm.Model
	ID       uint   `gorm:"primaryKey"`
	Password string `gorm:"not null" json:"password"`
	Username string `gorm:"unique_index;not null" json:"username"`
}
