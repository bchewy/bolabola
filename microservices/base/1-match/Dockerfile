# Use an official Node runtime as a base image
FROM node:21

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Bundle app source
COPY . .

# Define the command to run your application
CMD ["node", "index.js"]
