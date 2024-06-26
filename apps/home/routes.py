# -*- encoding: utf-8 -*-

from apps.home import blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.chatbotter import funcs

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/new_project', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form['name']
        project_type = request.form['type']  # Изменено имя переменной, т.к. 'type' является зарезервированным словом в Python
        company = request.form['company']
        status = int(request.form['status'])
        socials = request.form['socials']
        description = request.form.get('description', '')
        prompt = request.form.get('prompt', '')
        tg_token = request.form.get('tg_token', '')
        instagram_token = request.form.get('instagram_token', '')
        whatsapp_token = request.form.get('whatsapp_token', '')

        # Вызываем функцию для добавления нового проекта
        funcs.add_project_to_db(name=name, type=project_type, company=company, status=status,
                                socials=socials, description=description, prompt=prompt,
                                tg_token=tg_token, instagram_token=instagram_token,
                                whatsapp_token=whatsapp_token)

        # Перенаправляем пользователя на страницу со списком проектов
        return redirect(url_for('home_blueprint.projects'))

    # Для GET запроса просто отображаем форму
    return render_template('home/new-project.html')

@blueprint.route('/delete_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):
    # Используем вашу функцию для удаления проекта
    result = funcs.delete_project_by_id(project_id)
    message = result.get("message", "An error occurred.")
    if "successfully" in message:
        flash(message, 'success')
    else:
        flash(message, 'error')

    return redirect(url_for('home_blueprint.projects'))

@blueprint.route('/project', methods=['GET', 'POST'])
@login_required
def projects():
    segment = get_segment(request)

    project_list = funcs.get_all_projects()

    return render_template('home/project.html', segment=segment, project_list=project_list)

@blueprint.route('/config-project')
def config_project():
    project_id = request.args.get('projectId')
    if project_id:
        # Используем функцию get_project_by_id для получения данных проекта
        project = funcs.get_project_by_id(project_id)
        if project:
            return render_template('home/config-project.html', project=project)
    # Если проект не найден или project_id не предоставлен, перенаправляем на страницу списка проектов
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/update_project/<int:project_id>', methods=['POST'])
def update_project(project_id):
    try:
        # Используем project_id для получения текущего проекта
        project = funcs.get_project_by_id(project_id)
        if project:
            # Обновляем поля проекта данными из формы
            project.name = request.form.get('name')
            project.type = request.form.get('type')
            project.company = request.form.get('company')
            project.status = request.form.get('status')
            project.socials = request.form.get('socials')
            project.description = request.form.get('description')
            project.prompt = request.form.get('prompt')
            project.tg_token = request.form.get('tg_token')
            project.instagram_token = request.form.get('instagram_token')
            project.whatsapp_token = request.form.get('whatsapp_token')

            # Сохраняем изменения в базе данных
            funcs.update_project_in_db(project)

            flash('Project updated successfully.', 'success')
        else:
            flash('Project not found.', 'error')
    except Exception as e:
        flash(f'Error updating project: {e}', 'error')

    return redirect(url_for('home_blueprint.projects'))

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except:
        return render_template('home/page-500.html'), 500

def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return 'index'
