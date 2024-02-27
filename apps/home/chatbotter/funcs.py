from apps import db
from apps.authentication.models import Project

def add_project_to_db(name, type, company, status, socials, description='', prompt='', tg_token='', instagram_token='', whatsapp_token=''):

    new_project = Project(
        name=name,
        type=type,
        company=company,
        status=status,
        description=description,
        socials=socials,
        prompt=prompt,
        tg_token=tg_token,
        instagram_token=instagram_token,
        whatsapp_token=whatsapp_token)
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


def update_project_in_db(project, **kwargs):
    """
    Обновляет существующий проект в базе данных.

    :param project: Объект проекта с уже обновленными данными
    """
    try:
        db.session.add(project)  # Помечаем объект как "измененный" для сохранения в базе данных
        db.session.commit()
        # Возвращаем сообщение об успешном обновлении
        return {"message": "Project updated successfully"}, 200
    except Exception as e:
        # В случае ошибки при обновлении возвращаем сообщение об ошибке
        db.session.rollback()
        return {"message": f"Error updating project: {str(e)}"}, 500


def get_project_by_id(project_id):
    """
    Возвращает детали проекта по его ID.

    :param project_id: ID проекта
    :return: Словарь с информацией о проекте или None, если проект не найден
    """
    project = Project.query.get(project_id)
    if project:
        return project
        # return {
        #     "id": project.id,
        #     "name": project.name,
        #     "type": project.type,
        #     "company": project.company,
        #     "status": project.status,
        #     "description": project.description,
        #     "socials": project.socials,
        #     "prompt": project.prompt,
        #     "tg_token": project.tg_token,
        #     "instagram_token": project.instagram_token,
        #     "whatsapp_token": project.whatsapp_token
        # }
    return None


def delete_project_by_id(project_id):
    """
    Удаляет проект из базы данных по его ID.

    :param project_id: ID проекта для удаления
    :return: Словарь с сообщением о результате операции
    """
    project = Project.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        return {"message": "Project deleted successfully"}
    return {"message": "Project not found"}
