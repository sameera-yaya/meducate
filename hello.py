from flask import Flask, render_template

app = Flask(__name__)

@app.route('/meds')
def meds():
    return """
    <html>
    <head>
            <meta charset="utf-8">
                    <title>Meducate</title>
                    </head>
                    <body>
                            <h1>MEDUCATe</h1>
                                    <form>
                                                    <input type="search" placeholder="Search">
                                                            </form>
                                                            </body>
                                                            </html>
                                                            """
if __name__ == '__main__':
   app.run(debug=True)
