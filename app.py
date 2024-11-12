from website import create_app

application = create_app()

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)

#if __name__ == "__main__":
 #   app = create_app()
 #   app.run(debug=True)