#!/bin/bash
set -e

# ./.envファイルを読み込んで変数として参照できるようにする
source ./.env

# Imageをbuild
docker compose build
if [ $? -ne 0 ]; then
    echo "Failed to build the Docker image."
    return 1
else
    echo "Docker build success"
fi

# ECRに接続
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
if [ $? -ne 0 ]; then
    echo "Failed to login to ECR."
    return 1
else
    echo "ECR login success"
fi

# DockerイメージをECRにプッシュ
docker tag $DOCKER_IMAGE_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$DOCKER_IMAGE_NAME:$IMAGE_TAG
if [ $? -ne 0 ]; then
    echo "Failed to tag the Docker image."
    return 1
fi

docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$DOCKER_IMAGE_NAME:latest
if [ $? -ne 0 ]; then
    echo "Failed to push the Docker image to ECR."
    return 1
else
    echo "ECR push success"
fi

# ECRにプッシュしたイメージをlambdaに更新
aws lambda update-function-code --function-name $LAMBDA_FUNC_NAME --image-uri $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$DOCKER_IMAGE_NAME:$IMAGE_TAG > /dev/null 2> /tmp/aws_lambda_error.log

if [ $? -eq 0 ]; then
    echo "lambda update success"
else
    # エラーメッセージを表示する
    cat /tmp/aws_lambda_error.log
    return 1
fi

# 一時ファイルを削除
rm -f /tmp/aws_lambda_error.log
