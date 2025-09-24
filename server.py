from base import create_app
    
app = create_app()

# Punto de entrada de la aplicacion Flask
if __name__ == '__main__':
    app.run(port=5014, debug=True)

