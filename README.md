# MSc Cloud DevOpsSec Project

> Production-ready Flask web application with comprehensive DevSecOps pipeline, Infrastructure as Code, and automated deployment on AWS Elastic Beanstalk

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/Ughanze23/Msc-Cloud-devOps-Project)
[![Project Report](https://img.shields.io/badge/Report-Google%20Drive-green)](https://drive.google.com/file/d/1oOVRwdA6AeeAUp-n4pLKalE7zO491it7/view?usp=drive_link)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![Terraform](https://img.shields.io/badge/Terraform-Infrastructure-purple)](https://www.terraform.io/)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [DevSecOps Pipeline](#devsecops-pipeline)
- [Infrastructure as Code](#infrastructure-as-code)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Security Implementation](#security-implementation)
- [Monitoring & Observability](#monitoring--observability)
- [CI/CD Workflow](#cicd-workflow)
- [Quality Assurance](#quality-assurance)
- [Documentation](#documentation)
- [Best Practices](#best-practices)

## 🎯 Overview

This project represents a comprehensive implementation of DevSecOps principles in a modern cloud environment. Built as part of the MSc in Cloud Computing program at National College of Ireland, it demonstrates industry-standard practices in continuous integration, continuous deployment, infrastructure automation, and security integration.

The application is a Flask-based web platform deployed on AWS Elastic Beanstalk, featuring automated CI/CD pipelines, infrastructure provisioning with Terraform, security scanning at multiple stages, and comprehensive monitoring. This project showcases the complete lifecycle of cloud-native application development, from code commit to production deployment.

### Learning Objectives

- **DevOps Culture**: Collaboration between development and operations
- **Security Integration**: Shift-left security practices (DevSecOps)
- **Automation**: End-to-end automation of build, test, and deployment
- **Infrastructure as Code**: Reproducible and version-controlled infrastructure
- **Continuous Improvement**: Monitoring, feedback, and iterative enhancement

## 🏗️ Architecture

### System Architecture
![alt text](image-2.png)
![alt text](image-1.png)
### Architecture Components

1. **Application Layer**: Flask web application with modular design
2. **CI/CD Layer**: GitHub Actions for automated workflows
3. **Security Layer**: Integrated security scanning and compliance
4. **Infrastructure Layer**: AWS Elastic Beanstalk with supporting services
5. **Monitoring Layer**: CloudWatch for metrics and logging
6. **IaC Layer**: Terraform for infrastructure provisioning

## ✨ Features

### Application Features

#### Web Application
- **Flask Framework**: Lightweight and flexible Python web framework
- **Responsive UI**: Modern, mobile-friendly interface with HTML/CSS
- **Database Integration**: SQLite (development) / PostgreSQL (production)
- **Session Management**: Secure user session handling
- **RESTful API**: Well-structured API endpoints
- **Form Validation**: Input validation and sanitization

#### Security Features
- **Authentication**: User authentication and authorization
- **HTTPS Enforcement**: SSL/TLS encryption for data in transit
- **Security Headers**: HSTS, CSP, X-Frame-Options
- **Input Validation**: Protection against injection attacks
- **Session Security**: Secure cookie configuration
- **CSRF Protection**: Cross-Site Request Forgery prevention

### DevOps Features

#### Continuous Integration
- **Automated Testing**: Unit tests, integration tests
- **Code Quality Checks**: Linting, formatting validation
- **Security Scanning**: SAST, dependency scanning
- **Build Automation**: Automated application packaging
- **Artifact Management**: Build artifact storage and versioning

#### Continuous Deployment
- **Automated Deployment**: Push-to-deploy workflow
- **Environment Management**: Dev, staging, production environments
- **Rollback Capability**: Quick rollback to previous versions
- **Health Checks**: Automated health monitoring post-deployment
- **Zero-Downtime Deployment**: Blue-green deployment strategy

#### Infrastructure as Code
- **Terraform**: Infrastructure provisioning and management
- **Version Control**: Infrastructure changes tracked in Git
- **State Management**: Remote state storage in S3
- **Module Design**: Reusable infrastructure modules
- **Environment Parity**: Consistent environments across stages

## 🛠️ Technology Stack

### Application Stack

#### Backend
- **Python 3.8+**: Core programming language
- **Flask**: Web application framework
- **SQLAlchemy**: ORM for database operations
- **Jinja2**: Template engine for HTML rendering
- **Werkzeug**: WSGI utilities and security features

#### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: Responsive styling with Flexbox/Grid
- **JavaScript**: Client-side interactivity
- **Bootstrap** (optional): UI component library

### Infrastructure & Deployment

#### AWS Services
- **Elastic Beanstalk**: Application deployment and management
- **EC2**: Compute instances for application hosting
- **RDS**: Managed relational database service
- **S3**: Object storage for static assets and logs
- **CloudWatch**: Monitoring and logging
- **IAM**: Identity and access management
- **VPC**: Network isolation and security

#### Infrastructure as Code
- **Terraform**: Infrastructure provisioning
- **HCL**: HashiCorp Configuration Language
- **AWS Provider**: Terraform AWS integration

### DevOps Tools

#### CI/CD
- **GitHub Actions**: Workflow automation
- **GitHub Secrets**: Secure credential management
- **GitHub Packages**: Artifact registry

#### Security Tools
- **SonarQube**: Static code analysis and quality gates
- **Snyk/Dependabot**: Dependency vulnerability scanning
- **Bandit**: Python security linting
- **TruffleHog**: Secret detection
- **OWASP ZAP**: Dynamic application security testing

#### Quality Assurance
- **pytest**: Python testing framework
- **Coverage.py**: Code coverage measurement
- **pylint**: Python code linting
- **black**: Code formatting
- **mypy**: Static type checking

## 🔒 DevSecOps Pipeline

### Security Integration Points

The pipeline integrates security at every stage (shift-left approach):

#### Stage 1: Pre-Commit (Developer Workstation)
- Git hooks for local validation
- Pre-commit framework for automated checks
- Local security scanning

#### Stage 2: Code Commit
- **Secret Detection**: Scan for hardcoded credentials
- **Dependency Check**: Vulnerable dependency identification
- **License Compliance**: Open-source license verification

#### Stage 3: Build
- **SAST**: Static Application Security Testing
- **Container Scanning**: Docker image vulnerability scanning
- **Quality Gates**: SonarQube quality and security gates

#### Stage 4: Test
- **Security Tests**: Automated security test cases
- **Compliance Tests**: Regulatory compliance validation
- **Penetration Tests**: Automated security testing

#### Stage 5: Deploy
- **Infrastructure Scanning**: Terraform security scanning
- **Configuration Validation**: Security configuration checks
- **Runtime Protection**: WAF and runtime security

#### Stage 6: Production
- **Continuous Monitoring**: Real-time security monitoring
- **Incident Response**: Automated alerting and response
- **Compliance Reporting**: Ongoing compliance validation

### Pipeline Workflow

![alt text](image.png)
```yaml
# Simplified GitHub Actions workflow
name: DevSecOps Pipeline

on: [push, pull_request]

jobs:
  security-scan:
    - Secret detection
    - Dependency scanning
    
  build:
    - Install dependencies
    - Run linters
    - Build application
    
  test:
    - Unit tests
    - Integration tests
    - Code coverage
    
  code-quality:
    - SonarQube analysis
    - Quality gate validation
    
  deploy:
    - Package application
    - Deploy to Elastic Beanstalk
    - Health check validation
    
  monitoring:
    - Configure CloudWatch alarms
    - Set up dashboards
```

## 🏗️ Infrastructure as Code

### Terraform Implementation

The project uses Terraform for complete infrastructure automation:

#### Infrastructure Components

**Network Layer:**
```hcl
# VPC, Subnets, Internet Gateway, Route Tables
module "vpc" {
  source = "./modules/vpc"
  
  cidr_block = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b"]
  public_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.3.0/24", "10.0.4.0/24"]
}
```

**Compute Layer:**
```hcl
# Elastic Beanstalk Application and Environment
resource "aws_elastic_beanstalk_application" "app" {
  name = "cloud-devops-app"
  description = "Cloud DevOps Project Application"
}

resource "aws_elastic_beanstalk_environment" "env" {
  name = "production"
  application = aws_elastic_beanstalk_application.app.name
  solution_stack_name = "64bit Amazon Linux 2 v3.3.11 running Python 3.8"
  
  setting {
    namespace = "aws:autoscaling:asg"
    name = "MinSize"
    value = "2"
  }
  
  setting {
    namespace = "aws:autoscaling:asg"
    name = "MaxSize"
    value = "4"
  }
}
```

**Database Layer:**
```hcl
# RDS Database Instance
resource "aws_db_instance" "database" {
  identifier = "cloud-devops-db"
  engine = "postgres"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name = aws_db_subnet_group.database.name
  
  backup_retention_period = 7
  multi_az = true
}
```

### Terraform Best Practices

- **State Management**: Remote state in S3 with DynamoDB locking
- **Modules**: Reusable infrastructure components
- **Variables**: Parameterized configurations
- **Outputs**: Export important resource information
- **Workspaces**: Environment separation (dev, staging, prod)
- **Versioning**: Provider and module version constraints

## 📁 Project Structure

```
Msc-Cloud-devOps-Project/
├── .ebextensions/              # Elastic Beanstalk configuration
│   ├── 01_packages.config      # System packages
│   ├── 02_python.config        # Python environment
│   └── 03_nginx.config         # Web server config
├── .elasticbeanstalk/          # EB CLI configuration
│   └── config.yml              # EB environment settings
├── .github/
│   └── workflows/              # GitHub Actions workflows
│       ├── ci.yml              # Continuous Integration
│       ├── cd.yml              # Continuous Deployment
│       ├── security.yml        # Security scanning
│       └── quality.yml         # Code quality checks
├── terraform/                  # Infrastructure as Code
│   ├── main.tf                 # Main configuration
│   ├── variables.tf            # Input variables
│   ├── outputs.tf              # Output values
│   ├── backend.tf              # State configuration
│   ├── modules/                # Reusable modules
│   │   ├── vpc/               # VPC module
│   │   ├── security/          # Security groups
│   │   └── database/          # RDS module
│   └── environments/           # Environment-specific configs
│       ├── dev/
│       ├── staging/
│       └── production/
├── website/                    # Flask application
│   ├── __init__.py            # Application factory
│   ├── models.py              # Database models
│   ├── views.py               # Route handlers
│   ├── auth.py                # Authentication
│   ├── templates/             # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── ...
│   ├── static/                # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── utils/                 # Utility functions
├── instance/                   # Instance-specific files
│   └── database.db            # SQLite database (dev)
├── __pycache__/               # Python cache files
├── tests/                     # Test files
│   ├── test_models.py
│   ├── test_views.py
│   └── test_auth.py
├── .ebignore                  # EB deployment ignore
├── .gitignore                 # Git ignore rules
├── application.py             # Application entry point
├── requirements.txt           # Python dependencies
├── sonar-project.properties   # SonarQube configuration
├── Dockerfile                 # Container definition
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

#### Required Software
- **Python**: 3.8 or higher
- **AWS CLI**: Configured with credentials
- **EB CLI**: Elastic Beanstalk Command Line Interface
- **Terraform**: Version 1.0+
- **Git**: Version control
- **Docker** (optional): For local containerized development

#### AWS Requirements
- Active AWS account
- IAM user with appropriate permissions:
  - Elastic Beanstalk
  - EC2
  - RDS
  - S3
  - CloudWatch
  - IAM (for role creation)

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/Ughanze23/Msc-Cloud-devOps-Project.git
cd Msc-Cloud-devOps-Project
```

#### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Environment Variables
```bash
# Create environment file
cp .env.example .env

# Edit .env with your configuration
# DATABASE_URL=postgresql://user:pass@localhost/dbname
# SECRET_KEY=your-secret-key
# FLASK_ENV=development
```

#### 4. Initialize Database
```bash
# Run database migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### 5. AWS Configuration
```bash
# Configure AWS CLI
aws configure

# Initialize Elastic Beanstalk
eb init -p python-3.8 cloud-devops-app --region us-east-1
```

### Running Locally

#### Development Server
```bash
# Set Flask environment variables
export FLASK_APP=application.py
export FLASK_ENV=development

# Run the development server
flask run

# Application available at http://localhost:5000
```

#### Using Docker
```bash
# Build Docker image
docker build -t cloud-devops-app .

# Run container
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  cloud-devops-app
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=website --cov-report=html

# Run specific test file
pytest tests/test_views.py

# Run linting
pylint website/
black --check website/
```

## 📦 Deployment

### Elastic Beanstalk Deployment

#### Using EB CLI

```bash
# Create environment
eb create production --database.engine postgres

# Deploy application
eb deploy

# Check status
eb status

# View logs
eb logs

# Open in browser
eb open
```

#### Using GitHub Actions

Deployment is automated via GitHub Actions:

1. **Push to main branch** triggers deployment
2. **Tests run** to ensure code quality
3. **Security scans** validate no vulnerabilities
4. **Build artifacts** are created
5. **Deploy to AWS** Elastic Beanstalk
6. **Health checks** verify deployment success

### Infrastructure Deployment with Terraform

```bash
cd terraform

# Initialize Terraform
terraform init

# Plan infrastructure changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# View outputs
terraform output

# Destroy infrastructure (if needed)
terraform destroy
```

### Environment Configuration

#### Development
```bash
eb use development
eb deploy
```

#### Staging
```bash
eb use staging
eb deploy
```

#### Production
```bash
eb use production
eb deploy
```

## 🔐 Security Implementation

### Security Layers

#### 1. Application Security
- **Input Validation**: Sanitize all user inputs
- **Output Encoding**: Prevent XSS attacks
- **SQL Injection Prevention**: Parameterized queries via SQLAlchemy
- **CSRF Protection**: Token-based CSRF prevention
- **Session Security**: Secure, HTTPOnly, SameSite cookies

#### 2. Infrastructure Security
- **VPC Isolation**: Private subnets for databases
- **Security Groups**: Least-privilege network access
- **NACL**: Network-level access control
- **Encryption**: EBS encryption, RDS encryption
- **Secrets Management**: AWS Secrets Manager / Parameter Store

#### 3. Authentication & Authorization
- **Password Hashing**: bcrypt/argon2 for password storage
- **Session Management**: Secure session handling
- **Role-Based Access Control**: Permission-based features
- **Multi-Factor Authentication**: Optional 2FA support

#### 4. Monitoring & Compliance
- **CloudWatch**: Centralized logging
- **CloudTrail**: API call auditing
- **AWS Config**: Configuration compliance
- **Security Hub**: Centralized security findings

### Security Best Practices Implemented

- ✅ Principle of least privilege
- ✅ Defense in depth
- ✅ Secure defaults
- ✅ Fail securely
- ✅ Regular security updates
- ✅ Security logging and monitoring
- ✅ Input validation
- ✅ Output encoding
- ✅ Encryption everywhere
- ✅ Security testing in CI/CD

## 📊 Monitoring & Observability

### CloudWatch Integration

#### Metrics Monitored
- **Application Metrics**
  - Request count and latency
  - Error rates (4xx, 5xx)
  - Response times
  - Active connections

- **System Metrics**
  - CPU utilization
  - Memory usage
  - Disk I/O
  - Network throughput

- **Custom Metrics**
  - Business KPIs
  - User activity
  - Feature usage

#### Logging
- **Application Logs**: Structured JSON logging
- **Access Logs**: Request/response logging
- **Error Logs**: Exception tracking
- **Audit Logs**: Security events

#### Alarms
- High error rate (>5% 5xx errors)
- High latency (>2s response time)
- Low disk space (<20%)
- High CPU usage (>80%)
- Database connection failures

### Dashboards

Custom CloudWatch dashboards for:
- Real-time application health
- Infrastructure performance
- Security events
- Business metrics
- Cost tracking

## 🔄 CI/CD Workflow

### GitHub Actions Workflow

#### 1. Pull Request Workflow
```yaml
name: PR Validation
on: [pull_request]

jobs:
  validate:
    - Code formatting check
    - Linting
    - Unit tests
    - Security scan
    - SonarQube analysis
```

#### 2. Main Branch Workflow
```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  test:
    - Run full test suite
    - Generate coverage report
    
  security:
    - Dependency scanning
    - Secret detection
    - Container scanning
    
  build:
    - Build application
    - Create deployment package
    
  deploy:
    - Deploy to Elastic Beanstalk
    - Run health checks
    - Notify team
```

#### 3. Scheduled Workflows
- **Daily**: Security scans
- **Weekly**: Dependency updates
- **Monthly**: Performance testing

## 🎯 Quality Assurance

### SonarQube Integration

**Quality Gates:**
- Code coverage > 80%
- No critical bugs
- Technical debt ratio < 5%
- No blocker issues
- Security rating A

**Metrics Tracked:**
- Code smells
- Bugs and vulnerabilities
- Code duplication
- Complexity
- Maintainability rating

### Code Quality Standards

- **PEP 8**: Python style guide compliance
- **Type Hints**: Type annotations for better IDE support
- **Documentation**: Docstrings for all public functions
- **Test Coverage**: Minimum 80% coverage


## 📚 Documentation

Comprehensive documentation includes:

- **[Project Report](https://drive.google.com/file/d/1oOVRwdA6AeeAUp-n4pLKalE7zO491it7/view?usp=drive_link)**: Complete academic documentation
- **Architecture Documentation**: System design and diagrams
- **API Documentation**: Endpoint specifications
- **Deployment Guide**: Step-by-step deployment instructions


## 🏆 Best Practices

### DevOps Principles
1. **Automation First**: Automate repetitive tasks
2. **Version Everything**: Code, infrastructure, configuration
3. **Test Early, Test Often**: Comprehensive testing at all stages
4. **Monitor Everything**: Metrics, logs, traces
5. **Fail Fast**: Quick feedback loops
6. **Continuous Improvement**: Regular retrospectives

### Security Principles
1. **Shift Left**: Security from the start
2. **Least Privilege**: Minimal necessary permissions
3. **Defense in Depth**: Multiple security layers
4. **Zero Trust**: Never trust, always verify
5. **Encryption Everywhere**: Data at rest and in transit

### Cloud Principles
1. **Infrastructure as Code**: All infrastructure version-controlled
2. **Immutable Infrastructure**: Replace, don't update
3. **Scalability**: Design for horizontal scaling
4. **Resilience**: Handle failures gracefully
5. **Cost Optimization**: Monitor and optimize costs

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow coding standards
4. Write tests
5. Update documentation
6. Submit pull request

## 📄 License

Academic project for MSc Cloud Computing program at National College of Ireland.

## 👨‍💻 Author

**Ikenna Ughanze**
- GitHub: [@Ughanze23](https://github.com/Ughanze23)
- Institution: National College of Ireland
- Course: Cloud DevOpsSec

## 🙏 Acknowledgments

- National College of Ireland for academic guidance
- AWS for educational resources

## 📞 Support

- **Issues**: GitHub Issues for bug reports
- **Documentation**: Comprehensive docs in repository
- **Academic**: Course instructors and teaching assistants

---

**Project Highlights:**
- ✅ Complete DevSecOps implementation
- ✅ Production-ready Flask application
- ✅ Infrastructure as Code with Terraform
- ✅ Automated CI/CD with GitHub Actions
- ✅ Comprehensive security integration
- ✅ AWS Elastic Beanstalk deployment
- ✅ SonarQube quality gates
- ✅ CloudWatch monitoring
- ✅ 146 commits demonstrating iterative development

This project represents industry-standard DevOps and cloud engineering practices, suitable for real-world enterprise applications.
