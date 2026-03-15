from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Event, Session, Speaker, Bio, SessionSpeaker

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return jsonify({"message": "API is running"}), 200


# EVENT ENDPOINTS

@app.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    events_data = [
        {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        for event in events
    ]
    return jsonify(events_data), 200


@app.route("/events/<int:id>/sessions", methods=["GET"])
def get_event_sessions(id):
    event = Event.query.get(id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    sessions_data = [
        {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat()
        }
        for session in event.sessions
    ]
    return jsonify(sessions_data), 200


# SPEAKER ENDPOINTS

@app.route("/speakers", methods=["GET"])
def get_speakers():
    speakers = Speaker.query.all()
    speakers_data = [
        {
            "id": speaker.id,
            "name": speaker.name
        }
        for speaker in speakers
    ]
    return jsonify(speakers_data), 200


@app.route("/speakers/<int:id>", methods=["GET"])
def get_speaker(id):
    speaker = Speaker.query.get(id)

    if speaker is None:
        return jsonify({"error": "Speaker not found"}), 404

    speaker_data = {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
    }
    return jsonify(speaker_data), 200


# SESSION ENDPOINTS

@app.route("/sessions/<int:id>/speakers", methods=["GET"])
def get_session_speakers(id):
    session = Session.query.get(id)

    if session is None:
        return jsonify({"error": "Session not found"}), 404

    speakers_data = [
        {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": speaker.bio.bio_text if speaker.bio else "No bio available"
        }
        for speaker in session.speakers
    ]
    return jsonify(speakers_data), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)