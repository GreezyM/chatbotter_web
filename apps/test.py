from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy import Column, Integer, String
from apps.home.chatbotter import funcs
from run import app
def main():



    # with app.app_context():
    #     funcs.add_project_to_db(
    #         name="ProService",
    #         type="neuro-consult",
    #         company="Proservice",
    #         status=0,
    #         description="Здесь должно и может быть описание проекта или дедлайнов",
    #         socials="001"
    #     )












    # engine = create_engine("sqlite:///projects.sqlite3")
    #
    # metadata = MetaData()
    #
    # projects = Table(
    #     "projects",
    #     metadata,
    #     Column("id", Integer, primary_key=True, autoincrement=True),
    #     Column("name", String, nullable=False),
    #     Column("type", String, nullable=False),
    #     Column("company", String, nullable=False),
    #     Column("status", String, nullable=False),
    #     Column("description", String, nullable=False),
    #     Column("socials", String, nullable=False),
    # )
    #
    # metadata.create_all(engine)


if __name__ == '__main__':
    main()
