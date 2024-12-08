# Elastic Beanstalk Environment
resource "aws_elastic_beanstalk_environment" "flask_app_env" {
  name                = "cds-flask-app-env-3"
  application         = aws_elastic_beanstalk_application.flask_app.name
  solution_stack_name = "64bit Amazon Linux 2023 v4.3.1 running Python 3.9"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "LaunchTemplate"
    value     = "true"
  }

  # Instance Profile
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "arn:aws:iam::339712727128:instance-profile/MyEC2Role"
  }

  # Launch Template
  setting {
    namespace = "aws:ec2:launchtemplate"
    name      = "InstanceType"
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
