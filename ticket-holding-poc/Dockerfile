# Use the official Redis image as the base image
FROM redis:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the Redis configuration file to the container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose the default Redis port
EXPOSE 6379

# Start the Redis server with the custom configuration file
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
