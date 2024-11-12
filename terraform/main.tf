resource "aws_elastic_beanstalk_environment" "flask_app_env" {
  name                = "cds-flask-app-env"
  application         = aws_elastic_beanstalk_application.flask_app.name
  solution_stack_name = "64bit Amazon Linux 2023 v4.3.0 running Python 3.9"

  # Set the instance profile
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "LabInstanceProfile"  
  }

  # Set the service role
  setting {
    namespace  = "aws:elasticbeanstalk:environment"
    name       = "ServiceRole"
    value      = "LabRole"  
  }

  # Additional settings for environment capacity
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
