pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'subscription-manager'
        DOCKER_TAG = "${BUILD_NUMBER}"
        // Add registry credentials if needed
        // DOCKER_REGISTRY_CREDENTIALS = credentials('docker-registry-credentials')
    }

    options {
        skipStagesAfterUnstable()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    python manage.py test
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Ensure docker-compose is available
                    sh '''
                        if ! [ -x "$(command -v docker-compose)" ]; then
                            curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                            chmod +x /usr/local/bin/docker-compose
                        fi
                    '''
                    
                    // Deploy using docker-compose
                    sh '''
                        docker-compose down || true
                        docker-compose up -d
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                // Clean up old images safely
                sh '''
                    if command -v docker &> /dev/null; then
                        docker image prune -f
                        docker container prune -f
                    fi
                '''
            }
        }
        success {
            echo 'Successfully built and deployed!'
        }
        failure {
            echo 'Build or deployment failed!'
        }
    }
}
