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
                echo 'Starting frontend container...'
                bat 'docker run -d --name hyderabad-frontend-jenkins -p 8888:80 hyderabad-frontend'
                echo '✅ Frontend container running at http://localhost:8888'
            }
        }
        stage('Install Python Dependencies') {
            steps {
                echo 'Installing Python packages...'
                bat '"C:\\Users\\27ran\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install --upgrade pip && "C:\\Users\\27ran\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install selenium pytest'
            }
        }
        stage('Run Selenium Tests - Places Page') {
            steps {
                echo 'Running Selenium tests for Places Page...'
                bat '"C:\\Users\\27ran\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pytest selenium_tests/places_page --junitxml=selenium_tests/places_page/report.xml'
            }
        }
        stage('Run Selenium Tests - Food Page') {
            steps {
                echo 'Running Selenium tests for Food Page...'
                bat '"C:\\Users\\27ran\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pytest selenium_tests/food_page --junitxml=selenium_tests/food_page/report.xml'
            }
        }
        stage('Archive Test Reports') {
            steps {
                echo 'Archiving test results for both modules...'
                junit 'selenium_tests/places_page/report.xml'
                junit 'selenium_tests/food_page/report.xml'
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
