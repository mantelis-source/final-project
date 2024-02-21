from app import create_app
# get app object 
app = create_app()

if __name__ == "__main__":
    # run application
    app.run(debug=True)