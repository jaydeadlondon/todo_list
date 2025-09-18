from app import db
from flask import render_template, redirect, url_for, request, flash, Blueprint
from .models import Task
from .forms import TaskForm, FilterForm


bp = Blueprint('todo', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    task_form = TaskForm()
    filter_form = FilterForm()
    
    if task_form.validate_on_submit():
        task = Task(title=task_form.title.data, description=task_form.description.data, priority=task_form.priority.data)
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully', 'success')
        return redirect(url_for('todo.index'))
    
    if filter_form.validate_on_submit():
        status = filter_form.status.data
        priority = filter_form.priority.data
        query = Task.query
        if status != 'all':
            query = query.filter_by(completed=(status == 'completed')) 
        if priority != 'all':
            query = query.filter_by(priority=priority)   
        tasks = query.all()
    else:
        tasks = Task.query.all()
    return render_template('index.html', task_form=task_form, filter_form=filter_form, tasks=tasks)


@bp.route('/toggle/<int:id>', methods=['POST'])
def toggle_task(id):
    task = Task.query.get_or_404(id)
    task.toggle_completed()
    db.session.commit()
    flash('Task toggled successfully', 'success')
    return redirect(url_for('todo.index'))


@bp.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully', 'success')
    return redirect(url_for('todo.index'))


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        db.session.commit()
        flash('Task updated successfully', 'success')
        return redirect(url_for('todo.index'))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.priority.data = task.priority
    return render_template('edit_task.html', form=form, task=task)