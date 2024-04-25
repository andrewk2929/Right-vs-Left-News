from website import create_app


if __name__ == "__main__":
    # run app with debuger
    app = create_app()
    app.run(debug=True)