from app import create_app

app = create_app()  # No change here, uses default DevelopmentConfig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # The debug setting can be controlled by the config class
