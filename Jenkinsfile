pipeline {
  agent any

  environment {
    VENV_DIR = 'backend/.venv'
  }

  stages {
    stage('Start Services') {
      steps {
        sh 'docker compose up -d'
      }
    }

    stage('Install Dependencies') {
      steps {
        sh '''
          python3 -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          . ${VENV_DIR}/bin/activate
          python3 -m pytest backend/tests/ --junitxml=test-results/results.xml
        '''
      }
    }
  }

  post {
    always {
      sh 'docker compose down'
      junit 'test-results/results.xml'
    }
  }
}
