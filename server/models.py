from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    sessions = db.relationship(
        'Session',
        back_populates='event',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Event {self.id}, {self.name}, {self.location}>"


class SessionSpeaker(db.Model):
    __tablename__ = 'session_speakers'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'), nullable=False)

    session = db.relationship('Session', back_populates='session_speakers')
    speaker = db.relationship('Speaker', back_populates='session_speakers')

    def __repr__(self):
        return f"<SessionSpeaker {self.id}, session_id={self.session_id}, speaker_id={self.speaker_id}>"


class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    event = db.relationship('Event', back_populates='sessions')

    session_speakers = db.relationship(
        'SessionSpeaker',
        back_populates='session',
        cascade='all, delete-orphan'
    )

    speakers = db.relationship(
        'Speaker',
        secondary='session_speakers',
        back_populates='sessions',
        overlaps="session_speakers,session,speaker"
    )

    def __repr__(self):
        return f"<Session {self.id}, {self.title}, {self.start_time}>"


class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    bio = db.relationship(
        'Bio',
        back_populates='speaker',
        uselist=False,
        cascade='all, delete-orphan'
    )

    session_speakers = db.relationship(
        'SessionSpeaker',
        back_populates='speaker',
        cascade='all, delete-orphan'
    )

    sessions = db.relationship(
        'Session',
        secondary='session_speakers',
        back_populates='speakers',
        overlaps="session_speakers,session,speaker"
    )

    def __repr__(self):
        return f"<Speaker {self.id}, {self.name}>"


class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.String, nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'), nullable=False, unique=True)

    speaker = db.relationship('Speaker', back_populates='bio')

    def __repr__(self):
        return f"<Bio {self.id}, speaker_id={self.speaker_id}>"