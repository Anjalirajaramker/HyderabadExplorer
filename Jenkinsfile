pipeline {
    agent any
    triggers { pollSCM('H/5 * * * *') }

    stages {
        stage('Checkout SCM') {
            steps { 
                git branch: 'main', url: 'https://github.com/Anjalirajaramker/HyderabadExplorer.git' 
            }
        }

        stage('Build Frontend Docker (Demo)') {
            steps {
                echo 'Building frontend Docker container (for demo purposes)...'
                bat 'docker build -f Dockerfile.frontend -t hyderabad-frontend .'
                echo '✅ Frontend Docker image built successfully!'
            }
        }

        stage('Run Frontend Container (Demo)') {
            steps {
                echo 'Stopping any existing demo container...'
                bat 'docker rm -f hyderabad-frontend-jenkins || echo Skipping'
                echo 'Starting frontend container (demo only)...'
                bat 'docker run -d --name hyderabad-frontend-jenkins -p 8888:80 hyderabad-frontend'
                bat 'timeout /t 5' // small wait to ensure container is ready
                echo '✅ Docker frontend container is running (demo). Selenium will use local HTTP server instead.'
            }
        }

        stage('Install Python Dependencies') {
            steps {
                echo 'Installing Python packages for Selenium...'
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
                echo 'Archiving test results...'
                junit 'selenium_tests/places_page/report.xml'
                junit 'selenium_tests/food_page/report.xml'
            }
        }

        stage('Stop Docker Frontend Container (Demo)') {
            steps {
                echo 'Stopping and removing Docker frontend container (demo)...'
                bat 'docker stop hyderabad-frontend-jenkins && docker rm hyderabad-frontend-jenkins || echo Skipping'
                echo '✅ Docker frontend container stopped and removed'
            }
        }
    }
}
