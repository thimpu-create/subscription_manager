pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'subscription-manager'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh '''
                    python3 -m pip install -r requirements.txt
                    python3 manage.py test
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy Local') {
            steps {
                sh '''
                    docker-compose -f docker-compose.local.yml down || true
                    docker-compose -f docker-compose.local.yml up -d
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
