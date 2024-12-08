# Configure Terraform backend using S3
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Elastic Beanstalk Application
resource "aws_elastic_beanstalk_application" "flask_app" {
  name        = "loan-business-glossary-app"
  description = "Loan Business Glossary Flask application deployed through CI/CD"
}

# Elastic Beanstalk Environment
resource "aws_elastic_beanstalk_environment" "flask_app_env" {
  name                = "cds-flask-app-env-3"
  application         = aws_elastic_beanstalk_application.flask_app.name
  solution_stack_name = "64bit Amazon Linux  v4.3.1 running Python 3.9" 

#launch template
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "DisableLaunchConfiguration"
    value     = "true"
  }

  # Instance Profile
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "arn:aws:iam::339712727128:instance-profile/MyEC2Role"
  }

  # Instance Type
  setting {
    namespace = "aws:ec2:instances"
    name      = "InstanceTypes"
    value     = "t2.micro"
  }
  
  # Auto Scaling Group Settings
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

  # Environment Type
  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "LoadBalanced"
  }

  # Load Balancer Type
  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "LoadBalancerType"
    value     = "application"
  }

  # Rolling Updates
  setting {
    namespace = "aws:autoscaling:updatepolicy:rollingupdate"
    name      = "RollingUpdateEnabled"
    value     = "true"
  }
}