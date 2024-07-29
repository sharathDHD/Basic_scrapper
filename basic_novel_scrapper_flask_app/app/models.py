from app import db
from sqlalchemy.sql import func

class NovelUrls(db.Model):
    __tablename__ = 'novel_urls'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    webpage_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    response_code =db.Column(db.Integer)
    aouther = db.Column(db.String)

class ChaptersList(db.Model):
    __tablename__ = 'chapters_list'

    id = db.Column(db.Integer, primary_key=True)
    novel_url_id = db.Column(db.Integer, db.ForeignKey('novel_urls.id'), nullable=False)
    chapter_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    webpage_data = db.Column(db.Text)
    response_code =db.Column(db.Integer)

class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String, nullable=False)
    operation = db.Column(db.String, nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    old_data = db.Column(db.JSON)
    new_data = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())