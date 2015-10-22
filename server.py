from flask import Flask, request, redirect, url_for, render_template
import re

app = Flask(__name__)
uploaded = []

@app.route('/')
def landing():
    formatted = check_format()
    unique = False
    sanitize = False
    if formatted:
        unique = check_ids()
        sanitize = check_sanitize()
    count = len(uploaded)
    percent = int((count / 100.0) * 100)
    success = 'progress-bar-info'
    if percent == 100 and formatted and unique:
        success = 'progress-bar-success'
    if not sanitize or not unique or not formatted or percent > 100:
        success = 'progress-bar-danger'
    if formatted:
        format_style = 'alert-success'
    else:
        format_style = 'alert-danger'
    if unique:
        unique_style = 'alert-success'
    else:
        unique_style = 'alert-danger'
    if sanitize:
        sanitize_style = 'alert-success'
    else:
        sanitize_style = 'alert-danger'
    args = {'unique': unique_style, 'format': format_style, 'count':count,
            'percent':percent, 'success': success, 'sanitize': sanitize_style}
    return render_template('index.html', args=args)

@app.route('/image', methods=['POST'])
def images():
    uploaded.append(request.json)
    return 'total uploads {}'.format(len(uploaded))

@app.route('/purge')
def purge():
    global uploaded
    uploaded = []
    return redirect(url_for('landing'))
    

def check_ids():
    ids = []
    for data in uploaded:
        if data['id'] in ids:
            return False
        else:
            ids.append(data['id'])
    return True

def check_format():
    for data in uploaded:
        if type(data) != type({}):
            return False
        if 'id' not in data.keys():
            return False
        if 'type' not in data.keys():
            return False
        if 'file_path' not in data.keys():
            return False
        if 'notes' not in data.keys():
            return False
    return True

pattern = re.compile('UAMS_\d+')
def check_sanitize():
    for data in uploaded:
        for note in data['notes']:
            if pattern.match(str(note)):
                return False
        if pattern.match(str(data['id'])):
            return False
    return True


if __name__ == '__main__':
    app.debug = True
    app.run()
