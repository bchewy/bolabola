package util

import (
	// "log"
	// "encoding/json"
	"github.com/golang-jwt/jwt"
	// "net/http"
	"time"
	"math/rand"
)

func RandomString(n int) string {
	var letters = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
	s := make([]rune, n)
	for i := range s {
		s[i] = letters[rand.Intn(len(letters))]
	}
	return string(s)
}

func GenerateJWT(userId string, expiryMins int) (string, string, error) {
	secretKey := []byte(RandomString(16))

	token := jwt.New(jwt.SigningMethodHS256)
	claims := token.Claims.(jwt.MapClaims)
	claims["exp"] = time.Now().Add(time.Duration(expiryMins) * time.Minute)
	claims["authorized"] = true
	claims["user"] = userId

	tokenString, err := token.SignedString(secretKey)
	if err != nil {
		return "", "", err
	}

	return tokenString, string(secretKey), nil
}