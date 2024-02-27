# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.chatbotter import funcs
import json


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

        # Перенаправляем пользователя на страницу со списком проектов или на другую страницу
        return redirect(url_for('home_blueprint.index'))  # 'index' - название функции представления для главной страницы/списка проектов

    # Для GET запроса просто отображаем форму
    return render_template('home/new-project.html')


@blueprint.route('/project',methods=['GET', 'POST'])
@login_required
def project_template():
    segment = get_segment(request)

    project_list = funcs.get_all_projects()

    return render_template('home/project.html', segment=segment, project_list=project_list)

@blueprint.route('/config-project')
def config_project():
    project_id = request.args.get('projectId')
    if project_id:
        project = Project.query.filter_by(id=project_id).first()
        if project:
            return render_template('config-project.html', project=project)
    return redirect(url_for('your_fallback_route'))

@blueprint.route('/config-project.html')
def config_project():
    project_id = request.args.get('projectId')

    print(project_id)
    # Здесь вы загружаете данные проекта из базы данных по project_id
    # и передаете их в шаблон
    return render_template('home/config-project.html', project_data="project_data")


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


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'
        elif segment == 'config-project':
            segment = "project"

        return segment

    except:
        return None
