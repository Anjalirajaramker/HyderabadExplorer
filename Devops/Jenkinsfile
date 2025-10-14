pipeline {
    agent any
    triggers {
        pollSCM('H/5 * * * *') // Poll every 5 minutes
    }
    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Anjalirajaramker/HyderabadExplorer.git',
                    credentialsId: 'github-creds'
            }
        }
        stage('Verify  Files') {
            steps {
                echo 'Listing  project files...'
                sh 'ls -l'
                echo '✅  code checkout successful!'
            }
        }
    }
}
