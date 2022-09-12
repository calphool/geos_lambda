resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


data "aws_ecr_repository" "service" {
    name = "lambda-container"
}



resource "aws_lambda_function" "test_lambda" {
  function_name = "lambda_container"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "app.handler"
  runtime       = "python3.8"
  image_uri     = "${data.aws_ecr_repository.service.repository_url}:1"
  package_type  = "Image"


}