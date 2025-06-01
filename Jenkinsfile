pipeline {
    agent any

    parameters  {
        string(name: 'env', defaultValue: 'qa', values: 'qa', 'env', 'prod')
    }

    stages  {

        stage('Clone repo') {

            steps {
                git 'https://github.com/navneetkrishna/test_repo'
            }
        }

        stage('Run script') {

            steps{
                bat 'python main.py %env%'
            }
        }

    }
}