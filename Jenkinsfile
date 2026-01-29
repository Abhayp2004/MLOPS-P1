pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        GCP_PROJECT = "project-901d41e4-9c7e-4942-a40"
        REGION = "us-central1"
        IMAGE_NAME = "mlops-project"
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
                sh "python3 -m venv ${VENV_DIR}"
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

        stage('Upload dataset to GCS') {
            steps {
                echo "☁️ Uploading dataset to GCS..."
                sh "gsutil cp Hotel_Reservations.csv gs://my_bucket2004/"
            }
        }

        stage('Build Docker image') {
            steps {
                echo "🐳 Building Docker image..."

                sh """
                    docker build -t ${REGION}-docker.pkg.dev/${GCP_PROJECT}/mlops-repo/${IMAGE_NAME}:latest .
                """
            }
        }

        stage('Push image to Artifact Registry') {
            steps {
                echo "📤 Pushing image to Artifact Registry..."

                sh """
                    gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
                    docker push ${REGION}-docker.pkg.dev/${GCP_PROJECT}/mlops-repo/${IMAGE_NAME}:latest
                """
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                echo "🚀 Deploying to Cloud Run..."

                sh """
                    gcloud run deploy ml-project \
                      --image ${REGION}-docker.pkg.dev/${GCP_PROJECT}/mlops-repo/${IMAGE_NAME}:latest \
                      --platform managed \
                      --region ${REGION} \
                      --allow-unauthenticated \
                      --quiet
                """
            }
        }
    }
}
