import os

# Set default environment variables for database connection
# setdefault() is used to avoid overwriting existing environment variables

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5442")
os.environ.setdefault("DB_NAME", "concrete")
os.environ.setdefault("DB_USER", "user")
os.environ.setdefault("DB_PASSWORD", "password")