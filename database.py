"""Database models and setup for Gantt Chart application."""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Project(Base):
    """Project model - contains multiple tasks."""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to tasks
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Task(Base):
    """Task model - belongs to a project."""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    progress = Column(Float, default=0)  # 0-100
    completed = Column(Integer, default=0)  # 0 or 1 (boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to project
    project = relationship("Project", back_populates="tasks")
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'start': self.start_date.strftime('%Y-%m-%d'),
            'end': self.end_date.strftime('%Y-%m-%d'),
            'progress': self.progress,
            'project_id': self.project_id,
            'description': self.description or '',
            'completed': self.completed,
        }


# Database setup
DATABASE_URL = "sqlite:///./gantt.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Initialize the database, creating all tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Don't close here, will be closed by caller


def seed_sample_data():
    """Add sample data for testing (optional)."""
    db = get_db()
    
    # Check if we already have data
    if db.query(Project).count() > 0:
        db.close()
        return
    
    # Create sample project
    project = Project(
        name="Website Redesign",
        description="Complete redesign of company website"
    )
    db.add(project)
    db.commit()
    
    # Create sample tasks
    tasks = [
        Task(
            project_id=project.id,
            name="Design mockups",
            description="Create wireframes and high-fidelity mockups for all pages",
            start_date=datetime(2025, 2, 10),
            end_date=datetime(2025, 2, 20),
            progress=75
        ),
        Task(
            project_id=project.id,
            name="Frontend development",
            description="Build responsive UI components using React",
            start_date=datetime(2025, 2, 21),
            end_date=datetime(2025, 3, 10),
            progress=30
        ),
        Task(
            project_id=project.id,
            name="Backend integration",
            description="Connect frontend to REST API endpoints",
            start_date=datetime(2025, 3, 5),
            end_date=datetime(2025, 3, 20),
            progress=0
        ),
    ]
    
    for task in tasks:
        db.add(task)
    
    db.commit()
    db.close()
