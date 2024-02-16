package awsutil

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
)

func SetupAWSSession() *session.Session {
	creds := credentials.NewEnvCredentials()

	return session.Must(session.NewSessionWithOptions(session.Options{
		Profile:  "default",
		Config: aws.Config{
			Region: 	 aws.String("ap-southeast-1"),
			Credentials: creds,
		},
	}))
}

func SendToSQS(sess *session.Session, queueUrl string, messageBody string) error {
	sqsClient := sqs.New(sess)

	_, err := sqsClient.SendMessage(&sqs.SendMessageInput{
		QueueUrl:				&queueUrl,
		MessageBody:			aws.String(messageBody),
		MessageGroupId: 		aws.String("waiting-room-queue"),
		MessageDeduplicationId: aws.String("waiting"),
	})

	return err
}

func ConsumeFromSQS(sqsClient *sqs.SQS, queueUrl string) (*sqs.ReceiveMessageOutput, error) {

	return sqsClient.ReceiveMessage(&sqs.ReceiveMessageInput{
		QueueUrl:            aws.String(queueUrl),
		MaxNumberOfMessages: aws.Int64(1),
		VisibilityTimeout:   aws.Int64(30),  // 30 seconds
		WaitTimeSeconds:     aws.Int64(0),
	})
}