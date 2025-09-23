#!/bin/bash

# Create ssl directory if it doesn't exist
mkdir -p ssl

# Generate self-signed SSL certificate
openssl req -x509 -newkey rsa:2048 -nodes -days 365 \
  -keyout ssl/key.pem \
  -out ssl/cert.pem \
  -subj '/C=US/ST=CA/L=SanFrancisco/O=MyApp/OU=Dev/CN=member.bit.bio' \
  -addext 'subjectAltName=DNS:member.bit.bio,DNS:fs.capture.dev.workplaceservicing.co.uk,DNS:rdg.capture.dev.workplaceservicing.co.uk,DNS:localhost'

echo "SSL certificates generated successfully!"
ls -la ssl/
