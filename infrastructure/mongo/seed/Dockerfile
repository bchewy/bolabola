FROM mongo:latest

# Copy the JSON data and the scripts
COPY init.json /app/init.json
COPY entrypoint.sh /app/entrypoint.sh
# COPY wait-for-it.sh /app/wait-for-it.sh

# Make scripts executable
RUN chmod +x /app/entrypoint.sh 

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
