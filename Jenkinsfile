pipeline {
  agent any

  environment {
    BUILD_TAG_LOWER = "${BUILD_TAG}".toLowerCase().replaceAll('[^a-z0-9-]', '_')
    PYTHONPATH = "${WORKSPACE}/backend"
    VENV_DIR = 'backend/.venv'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        echo "Building branch: ${env.BRANCH_NAME ?: 'main'}"
        echo "Build number: ${env.BUILD_NUMBER}"
        echo "Docker Compose name: ${BUILD_TAG_LOWER}"
      }
    }

    stage('Start Services') {
      steps {
        sh "docker compose -f docker-compose-ci.yml --project-name '${BUILD_TAG_LOWER}' up -d"
        script {
          def mysqlPort = sh(
            script: "docker compose -f docker-compose-ci.yml --project-name '${BUILD_TAG_LOWER}' port mysql 3306 | cut -d: -f2",
            returnStdout: true
          ).trim()
          env.MYSQL_PORT = mysqlPort
          echo "MySQL starting on port ${mysqlPort}..."
        }
        sh 'sleep 5'
      }
    }

    stage('Install Dependencies') {
      steps {
        sh '''
          python3 -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          pip install -r backend/requirements.txt
        '''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          . ${VENV_DIR}/bin/activate
          python3 -m pytest backend/tests/ \
            --junitxml=test-results/results.xml \
            --maxfail=5 \
            -v
        '''
      }
    }
  }

  post {
    always {
      sh 'docker compose down -v || true'
      sh 'docker run --rm -v $(pwd):/workspace -w /workspace mysql sh -c "rm -rf tmp || true"'
      sh 'docker container prune -f || true'

      junit allowEmptyResults: true,
            testResults: 'test-results/results.xml',
            skipPublishingChecks: true

      archiveArtifacts artifacts: 'test-results/**/*',
                       allowEmptyArchive: true,
                       fingerprint: true

      sh '''
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete 2>/dev/null || true
        find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
      '''
    }

    success {
      echo 'All tests passed.'
    }

    failure {
      echo 'Build failed, check test results.'
    }
  }
}
