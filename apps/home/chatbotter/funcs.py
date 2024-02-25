from apps import db
from apps.authentication.models import Project

def add_project_to_db(name, type, company, status, description='', socials=''):
    """
    Добавляет проект в базу данных.

    :param name: Название проекта
    :param type: Тип проекта
    :param company: Компания, к которой относится проект
    :param status: Статус проекта
    :param description: Описание проекта (необязательно)
    :param socials: Социальные сети проекта (необязательно)
    """
    new_project = Project(name=name, type=type, company=company, status=status, description=description, socials=socials)
    db.session.add(new_project)
    db.session.commit()


def get_all_projects():
    """
    Возвращает список всех проектов в базе данных.
    """
    projects = Project.query.all()
    return [
        {
            "id": project.id,
            "name": project.name,
            "type": project.type,
            "company": project.company,
            "status": project.status,
            "description": project.description,
            "socials": project.socials
        } for project in projects
    ]


def update_project_in_db(project_id, **kwargs):
    """
    Обновляет существующий проект в базе данных по его id.

    :param project_id: ID проекта для обновления
    :param kwargs: Поля проекта для обновления (name, type, company, status, description, socials)
    """
    project = Project.query.get(project_id)
    if not project:
        return {"message": "Project not found"}, 404

    for key, value in kwargs.items():
        if hasattr(project, key):
            setattr(project, key, value)

    db.session.commit()
    return {"message": "Project updated successfully"}, 200
