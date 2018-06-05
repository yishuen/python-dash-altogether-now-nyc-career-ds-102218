from dashaltogethernow import app

if __name__ == '__main__':
    # adds in external css to style the table
    app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    app.run_server(debug=True)
