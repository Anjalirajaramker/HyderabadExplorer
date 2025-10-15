pipeline {
    agent any
    triggers { pollSCM('H/5 * * * *') }

    stages {
        stage('Checkout SCM') {
            steps { 
                git branch: 'main', url: 'https://github.com/Anjalirajaramker/HyderabadExplorer.git' 
            }
        }

        stage('Build Frontend Docker') {
            steps {
                echo 'Building frontend Docker container...'
                bat 'docker build -f Dockerfile.frontend -t hyderabad-frontend .'
                echo '✅ Frontend Docker image built successfully!'
            }
        }

        stage('Run Frontend Container') {
            steps {
                echo 'Stopping any existing frontend container...'
                bat 'docker rm -f hyderabad-frontend-jenkins || echo Skipping'
                echo 'Starting frontend container...'
                bat 'docker run -d --name hyderabad-frontend-jenkins -p 8888:80 hyderabad-frontend'
                echo '✅ Frontend container is running!'
                echo 'Frontend URL: http://localhost:8888'
            }
        }

        stage('Check Docker Status') {
            steps {
                echo 'Showing running Docker containers...'
                bat 'docker ps'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo 'Running Selenium tests (using local files, not Docker frontend)...'
                bat '"C:\\Users\\27ran\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install --upgrade pip selenium pytest'
                bat '"C:\\Users\\27ran\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pytest selenium_tests --junitxml=selenium_tests/report.xml'
            }
        }

        stage('Archive Test Reports') {
            steps {
                junit 'selenium_tests/report.xml'
            }
        }

        stage('Stop Frontend Container') {
            steps {
                echo 'Stopping and removing frontend container...'
                bat 'docker stop hyderabad-frontend-jenkins && docker rm hyderabad-frontend-jenkins'
                echo '✅ Frontend container stopped and removed'
            }
        }
    }
}
