pipeline {
    agent any
    triggers { pollSCM('H/5 * * * *') }
    stages {
        stage('Checkout SCM') {
            steps { git branch: 'main', url: 'https://github.com/Anjalirajaramker/HyderabadExplorer.git' }
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
    }
}

