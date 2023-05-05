import flask
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return flask.jsonify({'jobs': [item.to_dict() for item in users]})


"""@blueprint.route('/api/news/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify({'jobs': jobs.to_dict()})


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not flask.request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in flask.request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs = Jobs(
        team_leader=flask.request.json['team_leader'],
        job=flask.request.json['job'],
        work_size=flask.request.json['work_size'],
        collaborators=flask.request.json['collaborators'],
        start_date=flask.request.json['start_date'],
        end_date=flask.request.json['end_date'],
        is_finished=flask.request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})"""