# Portfolio Site

A containerized Flask application deployed on AWS ECS Fargate, built as a personal portfolio and as a hands-on cloud/DevOps project.

**Live site:** [elijahadebayo.com](https://elijahadebayo.com)

## Architecture

- **Application:** Flask, served by Gunicorn
- **Containerization:** Docker
- **Container registry:** Amazon ECR
- **Compute:** AWS ECS Fargate
- **Load balancing:** Application Load Balancer
- **Data:** DynamoDB (contact form submissions)
- **DNS / SSL:** Cloudflare (custom domain, HTTPS)

## Features

- About, Experience, Certifications, and Projects pages
- Contact form with server-side validation, writing to DynamoDB
- Health check endpoint (`/health`) used by the ECS/ALB health checks
- Environment-variable-driven configuration (region, table name), so the same image runs identically locally, in a container, and in ECS

## Running locally

\`\`\`bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
\`\`\`

## Running with Docker

\`\`\`bash
docker build -t portfolio-app .
docker run -p 5000:5000 --env AWS_REGION=eu-west-2 --env DYNAMODB_TABLE=portfolio-contact-messages portfolio-app
\`\`\`