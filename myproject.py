from app import app as application

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin',
                         '*')
    response.headers.add('Access-Control-Max-Age', 0)
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')    
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
    return response

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)