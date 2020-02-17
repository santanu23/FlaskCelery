from flask import Flask
from flask import url_for
from worker import celery
import celery.states as states
from celery import chain, group, signature

app = Flask(__name__)


@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response

@app.route('/process/')
def process() -> str:
    img_stitch_sig = signature('tasks.horizontal_stitch', args=[['test.png', 'test.png']])
    img_bright_sig = signature('tasks.increase_brightness', args=['test.png', 10])
    img_dark_sig = signature('tasks.decrease_brightness', args=['test.png', 10])
    img_histeg_sig = signature('tasks.histogram_eualization', args=['test.png'])
    res = group(img_stitch_sig, img_bright_sig, img_dark_sig, img_histeg_sig)()
    return 'done'

@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)