pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'subscription-manager'
        DOCKER_TAG = "${BUILD_NUMBER}"
        PYTHON_VERSION = '3.11'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 manage.py test'
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
                    // Install docker-compose if not present
                    sh '''
                        if ! [ -x "$(command -v docker-compose)" ]; then
                            sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                            sudo chmod +x /usr/local/bin/docker-compose
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
            cleanWs()
            script {
                try {
                    sh '''
                        docker system prune -f
                        docker image prune -f
                    '''
                } catch (err) {
                    echo "Docker cleanup failed: ${err}"
                }
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
