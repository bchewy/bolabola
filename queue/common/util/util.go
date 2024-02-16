package util

import (
	// "log"
	// "encoding/json"
	"github.com/golang-jwt/jwt"
	// "net/http"
	"time"
 )

func GenerateJWT(userId string, expiryMins int) (string, error) {
	testSecretKey := []byte("SecretKey")

	token := jwt.New(jwt.SigningMethodHS256)
	claims := token.Claims.(jwt.MapClaims)
	claims["exp"] = time.Now().Add(time.Duration(expiryMins) * time.Minute)
	claims["authorized"] = true
	claims["user"] = userId

	tokenString, err := token.SignedString(testSecretKey)
	if err != nil {
		return "", err
	}

	return tokenString, nil
}