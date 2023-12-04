pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
    }
    environment {
        ECR_REGISTRY       = '776201747781.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPOSITORY     = 'impulsea-app-be'
        DOCKER_IMAGE_TAG   = 'latest'
        ECS_CLUSTER        = 'impulsea-prod-app-cluster'
        AWS_DEFAULT_REGION = 'us-east-1'
        TASK_DEFINITION_BE = 'impulsea-prod-app-be'
    }
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
                sh 'docker system prune -a --volumes -f'
            }
        }
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh "docker build -t ${ECR_REPOSITORY} ."
            }
        }
        stage('Push') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: '7498ea59-ae72-4d8e-b83c-f7589ff2e93b',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                    sh "docker tag ${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}"
                    sh "docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}"
                }
            }
        }
        stage('Deploy') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: '7498ea59-ae72-4d8e-b83c-f7589ff2e93b',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh "aws ecs update-service --cluster ${ECS_CLUSTER} --service ${TASK_DEFINITION_BE} --force-new-deployment"
                }
            }
        }
        stage('Cleanup') {
            steps {
                sh 'docker system prune -a --volumes -f'
            }
        }
    }
}