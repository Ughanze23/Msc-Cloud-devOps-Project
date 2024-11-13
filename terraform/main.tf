# Configure Terraform backend using S3
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  
  backend "s3" {
    bucket = "x23384069-cpp"
    key    = "flask-app/terraform.tfstate"
    region = "us-east-1" 
  }
}

# Existing resources for your Elastic Beanstalk application

resource "aws_elastic_beanstalk_application" "flask_app" {
  name        = "loan-business-glossary-app"
  description = "Loan Business Glossary Flask application deployed through CI/CD"
}

resource "aws_elastic_beanstalk_environment" "flask_app_env" {
  name                = "cds-flask-app-env"
  application         = aws_elastic_beanstalk_application.flask_app.name
  solution_stack_name = "64bit Amazon Linux 2023 v4.3.0 running Python 3.9"

  # Add the instance profile reference
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "arn:aws:iam::205576784570:instance-profile/LabInstanceProfile"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = "t2.micro"
  }
  
  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MinSize"
    value     = "1"
  }
  
  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MaxSize"
    value     = "2"
  }
}