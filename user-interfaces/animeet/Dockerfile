# Use a Node.js base image
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --force

# Copy the rest of your application code
COPY . .

# Set the environment variable to disable ESLint during the build
# ENV NEXT_PUBLIC_ESLINT_DISABLE=true
ENV NEXT_DISABLE_ESLINT=1

# Build the Next.js application
RUN npm run build
# RUN next build

# # Use a minimal Node.js image for the final stage
FROM node:18-alpine

# # Set working directory
WORKDIR /app

# Copy the built files from the builder stage
COPY --from=builder /app . 

# Expose the Next.js default port
EXPOSE 3000

# Run the application in production mode
CMD ["npm", "run", "start"]