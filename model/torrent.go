package model

import 
	(
	"gorm.io/gorm"
)

type Torrent struct {
	gorm.Model
	ID       uint   `gorm:"primaryKey"`
	Location string `json:"location"`
	Magnet   string `json:"magnet"`
	Names    string `json:"names"`
	User     User   `gorm:"references:UserID"`
}
