# Use the official Node.js 14 image as the base image for the build stage
FROM node:16 as build-stage

# Set the working directory inside the container for the build stage
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install the app dependencies
RUN npm install

# Copy the rest of the app source code to the working directory
COPY . .

# Build the Vue app for production and output to the 'dist' directory
RUN npm run build

# Use the official nginx image as the base image for the production stage
FROM nginx:stable-alpine as production-stage

# Copy the built assets from the 'build-stage' to the nginx serving directory
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx-selfsigned.crt /etc/nginx/ssl/nginx-selfsigned.crt
COPY nginx-selfsigned.key /etc/nginx/ssl/nginx-selfsigned.key
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443

# Define the command to run the app using nginx
CMD ["nginx", "-g", "daemon off;"]
