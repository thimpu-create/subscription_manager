pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v $HOME/.cache:/root/.cache'
        }
    }

    environment {
        DOCKER_IMAGE = 'subscription-manager'
        DOCKER_TAG = "${BUILD_NUMBER}"
        HOME = '.'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python manage.py test'
            }
        }

        stage('Build Docker Image') {
            agent any  // Switch back to Jenkins agent for Docker commands
            steps {
                script {
                    try {
                        sh """
                            docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                        """
                    } catch (err) {
                        echo "Docker build failed: ${err}"
                        currentBuild.result = 'FAILURE'
                        error("Docker build failed")
                    }
                }
            }
        }

        stage('Deploy Local') {
            agent any  // Use Jenkins agent for deployment
            when {
                expression { currentBuild.result != 'FAILURE' }
            }
            steps {
                script {
                    try {
                        sh '''
                            docker-compose -f docker-compose.local.yml down || true
                            docker-compose -f docker-compose.local.yml up -d
                        '''
                    } catch (err) {
                        echo "Deployment failed: ${err}"
                        currentBuild.result = 'FAILURE'
                        error("Deployment failed")
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Build and deployment successful!'
        }
        failure {
            echo 'Build or deployment failed!'
        }
    }
}
