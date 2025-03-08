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

        stage('Install Dependencies') {
            steps {
                sh '''
                    # Install Python if not present
                    if ! command -v python3 &> /dev/null; then
                        sudo apt-get update
                        sudo apt-get install -y python3 python3-pip
                    fi

                    # Install Docker if not present
                    if ! command -v docker &> /dev/null; then
                        sudo apt-get update
                        sudo apt-get install -y docker.io
                        sudo systemctl start docker
                        sudo systemctl enable docker
                        sudo usermod -aG docker jenkins
                    fi

                    # Install docker-compose if not present
                    if ! command -v docker-compose &> /dev/null; then
                        sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                        sudo chmod +x /usr/local/bin/docker-compose
                    fi
                '''
            }
        }

        stage('Build Environment') {
            steps {
                sh '''
                    # Create and activate virtual environment
                    python3 -m pip install virtualenv
                    python3 -m virtualenv venv
                    . venv/bin/activate
                    
                    # Install requirements
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py test
                '''
            }
        }

        stage('Build Docker Image') {
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
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.result != 'FAILURE' }
            }
            steps {
                script {
                    try {
                        sh '''
                            docker-compose down || true
                            docker-compose up -d
                        '''
                    } catch (err) {
                        echo "Deployment failed: ${err}"
                        currentBuild.result = 'FAILURE'
                    }
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
                        if command -v docker &> /dev/null; then
                            docker system prune -f
                            docker image prune -f
                        fi
                    '''
                } catch (err) {
                    echo "Cleanup failed: ${err}"
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
