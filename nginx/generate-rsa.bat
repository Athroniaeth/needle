# Generate a private key
openssl genrsa -out localhost.key 2048

# Generate a self-signed certificate (valid for 365 days)
openssl req -new -x509 -key localhost.key -out localhost.crt -days 365 -subj "/CN=localhost"