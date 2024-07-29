from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app import db
from app.models import NovelUrls, ChaptersList, Log
import logging

def init_db(app):
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Create user if not exists
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 FROM pg_roles WHERE rolname='sharath'"))
            if not result.fetchone():
                connection.execute(text("CREATE USER sharath WITH PASSWORD 'k1ngd00m'"))
                connection.execute(text("ALTER USER sharath CREATEDB"))

        # Create triggers
        create_triggers()

def create_triggers():
    trigger_functions = [
        """
        CREATE OR REPLACE FUNCTION log_novel_urls_changes()
        RETURNS TRIGGER AS $$
        BEGIN
            IF (TG_OP = 'INSERT') THEN
                INSERT INTO log (table_name, operation, record_id)
                VALUES ('novel_urls', 'INSERT', NEW.id);
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO log (table_name, operation, record_id, old_data, new_data)
                VALUES ('novel_urls', 'UPDATE', NEW.id, row_to_json(OLD), row_to_json(NEW));
            ELSIF (TG_OP = 'DELETE') THEN
                INSERT INTO log (table_name, operation, record_id, old_data)
                VALUES ('novel_urls', 'DELETE', OLD.id, row_to_json(OLD));
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """,
        """
        CREATE OR REPLACE FUNCTION log_chapters_list_changes()
        RETURNS TRIGGER AS $$
        BEGIN
            IF (TG_OP = 'INSERT') THEN
                INSERT INTO log (table_name, operation, record_id)
                VALUES ('chapters_list', 'INSERT', NEW.id);
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO log (table_name, operation, record_id, old_data, new_data)
                VALUES ('chapters_list', 'UPDATE', NEW.id, row_to_json(OLD), row_to_json(NEW));
            ELSIF (TG_OP = 'DELETE') THEN
                INSERT INTO log (table_name, operation, record_id, old_data)
                VALUES ('chapters_list', 'DELETE', OLD.id, row_to_json(OLD));
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    ]

    triggers = [
        """
        CREATE TRIGGER novel_urls_audit
        AFTER INSERT OR UPDATE OR DELETE ON novel_urls
        FOR EACH ROW EXECUTE FUNCTION log_novel_urls_changes();
        """,
        """
        CREATE TRIGGER chapters_list_audit
        AFTER INSERT OR UPDATE OR DELETE ON chapters_list
        FOR EACH ROW EXECUTE FUNCTION log_chapters_list_changes();
        """
    ]

    engine = db.engine
    with engine.connect() as connection:
        for func in trigger_functions:
            connection.execute(text(func))
        
        for trigger in triggers:
            try:
                connection.execute(text(trigger))
            except Exception as e:
                logging.warning(f"Trigger already exists: {str(e)}")

def get_db_session():
    Session = sessionmaker(bind=db.engine)
    return Session()