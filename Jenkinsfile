pipeline {
    agent any
    
    // // Define environment variables
    // environment {
    //     DOCKER_IMAGE = 'myapp:latest'
    //     DEPLOY_ENV = 'staging'
    // }
    
    // Define pipeline stages
    stages {
        stage('Checkout') {
            steps {
                // Checkout code from repository
                sh 'echo checkout'
            }
        }
        
        stage('Build') {
            steps {
                // Example build steps
                sh 'echo build'
                
            
            }
        }
        
        stage('Unit Tests') {
            steps {
                sh 'echo test'
                
            
            }
        }
        
        stage('Code Analysis') {
            steps {
                 sh 'echo Code Analysis'
            }
        }
        
        stage('Docker Build') {
            steps {
                 sh 'echo Build'
            }
        }
        
        stage('Security Scan') {
            steps {
                // Run security scanning
                sh 'echo Security Scan'
            }
        }
        
  
        
       
    }
    
  
}
