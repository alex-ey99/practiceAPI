pipeline {
    agent {
        docker { image 'al9x9y/fileapp:1.0' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'python --version'
            }
        }
    }
}
