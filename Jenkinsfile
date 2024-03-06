pipeline {
  agent any
  stages {
    stage('get excel and python script') {
      steps {
        echo 'Getting the excel and python files'
        sh '''ls -la
chmod 754 CSV_formatter.py
chmod 754 prod_mp_upload_rules.py
chmod 754 prod_mp_redir_validation.py'''
      }
    }

    stage('Running formatter') {
      steps {
        echo 'Running CSV formatter and generating CSV files'
        sh 'python3 CSV_formatter.py'
        sh 'ls -la'
      }
    }

    stage('Upload Games') {
      steps {
        echo 'checking if there is a csv file for games'
        script {
          if (fileExists('mp-test-games-upload.csv')) {
            sh 'echo "uploading games rules"'
            sh 'python3 prod_mp_upload_rules.py mp-test-games-upload.csv'
          }
        }

      }
    }

    stage('Upload General') {
      steps {
        echo 'Checking for CSV for General'
        script {
          if (fileExists('mp-test-general-upload.csv')) {
            sh 'echo "uploading general rules"'
            sh 'python3 prod_mp_upload_rules.py mp-test-general-upload.csv'
          }
        }

      }
    }

    stage('Testing All Redirects') {
      steps {
        echo 'Testing the uploaded rules'
        script {
          if (fileExists('test-uploader2.xlsx')) {
            sh 'echo "testing uploaded rules"'
            sh 'python3 prod_mp_redir_validation.py'
          }
        }

      }
    }

    stage('Delete environment') {
      steps {
        cleanWs(cleanWhenAborted: true, cleanWhenFailure: true, cleanWhenNotBuilt: true, cleanWhenSuccess: true)
      }
    }

  }
}
