pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {

        stage('Clone GitHub Repo') {
            steps {
                echo "📥 Cloning GitHub repository..."

                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        credentialsId: 'github-token',
                        url: 'https://github.com/Abhayp2004/MLOPS-P1.git'
                    ]]
                )
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                echo "🐍 Creating virtual environment..."

                sh """
                    python3 -m venv ${VENV_DIR}
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "📦 Installing dependencies..."

                sh """
                    ${VENV_DIR}/bin/pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -r requirements.txt
                """
            }
        }

    }
}
