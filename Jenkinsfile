pipeline {
    agent any

    parameters {

        choice(name: 'env', choices: ['qa', 'env', 'prod'], description: 'Choose the environment')

    }


    stages  {

        stage('Clone repo') {

            steps {
                git 'https://github.com/navneetkrishna/test_repo'
            }
        }

        stage('Run script') {

            steps{
                bat "python main.py ${params.env}"
            }
        }

    }
}