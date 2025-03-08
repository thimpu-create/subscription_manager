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

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").inside {
                        sh 'python manage.py test'
                    }
                }
            }
        }

        stage('Collect Static') {
            steps {
                script {
                    docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").inside {
                        sh 'python manage.py collectstatic --noinput'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Stop existing container if running
                    sh 'docker-compose down || true'
                    
                    // Start new container
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        always {
            // Clean up old images
            sh 'docker system prune -f'
        }
    }
}
