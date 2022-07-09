package model

import "gorm.io/gorm"

// User struct
type User struct {
	gorm.Model
	Email    string `gorm:"unique_index;not null" json:"email"`
	ID       uint   `gorm:"primaryKey"`
	Names    string `json:"names"`
	Password string `gorm:"not null" json:"password"`
	Username string `gorm:"unique_index;not null" json:"username"`
}
