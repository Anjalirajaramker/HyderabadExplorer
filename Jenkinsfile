pipeline {
    agent any
    triggers { pollSCM('H/5 * * * *') }
    stages {
        stage('Checkout SCM') {
            steps { 
                git branch: 'main', url: 'https://github.com/Anjalirajaramker/HyderabadExplorer.git' 
            }
        }
        stage('Verify Frontend Files') { 
            steps {
                dir('Devops') {
                    echo 'Listing frontend project files...'
                    bat 'dir'
                    echo '✅ Frontend code checkout successful!'
                }
            }
        }
        stage('Copy Frontend Files for Preview') {
            steps {
                echo 'Copying frontend files to local preview folder...'
                bat '''
                if not exist C:\\JenkinsPreview\\HyderabadExplorer mkdir C:\\JenkinsPreview\\HyderabadExplorer
                xcopy /E /Y Devops\\* C:\\JenkinsPreview\\HyderabadExplorer\\
                '''
                echo '✅ Files copied! Ready to preview at C:\\JenkinsPreview\\HyderabadExplorer'
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
    }
}
