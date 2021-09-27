from flask import Flask
from flask_restful import Api, Resource, marshal_with, reqparse, abort, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)            # this saying we gonna wrap our class with an APi
app.config['SQLAlchemy_DATABASE_URL'] = 'sqlite:///database.db'    # this ///database.db is a path to the database.db file
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # primary_key: saying eveyry single video we store will have unique indentifier
    name = db.Column(db.String(100), nullable=False) # nullable: saying we must have this info
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

# db.create_all()         # only do this ***ONCE***, delete this line after a database is created already

# names = {"tim": {"age": 19, "gender": "male"}, 
#         "bill": {"age": 70, "gender": "male"}}

#class HelloWorld(Resource):   # "helloworld" will inherit "resource"
#    def get(self, name):            # overload the get() method, get request is sent to certain url
#        return names[name]                 # this phrase is returned whenever get request is done

video_put_args = reqparse.RequestParser()       # we gonna make a new RequestParser object that make sure the request follows correct guidelines
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)  # "help" is error message in case s.t failed
video_put_args.add_argument("views", type=str, help="Views of the video", required=True) 
video_put_args.add_argument("likes", type=str, help="Likes on the video", required=True) 

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

# videos = {}

# def abort_if_video_id_doesnt_exist(video_id):
#     if video_id not in videos:
#         abort(404, message="Could not find video...")       # from abort library, it send an abort message so that the program won't crash

# def abort_if_video_exists(video_id):
#     if video_id in videos:
#         abort(409, message="Video already exists with that ID...")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        # abort_if_video_id_doesnt_exist(video_id)    # this will make sure video_id exist before return --> prevent the crash
        result = VideoModel.query.filter_by(id=video_id).first()    # query here means this is going to create an instance of class VideoModel
        if not result:
            abort(404, message="Could not find video with that id")
        return result                                 # we need to serialize "result" to be able to return --> utilize resource_fields
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken...")

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()                 # commit and make them permanent in the database
        return video, 201       # 201 - means something is created

    @marshal_with(resource_fields)
    def patch(self, video_id):
		    args = video_update_args.parse_args()
		    result = VideoModel.query.filter_by(id=video_id).first()
		    if not result:
			    abort(404, message="Video doesn't exist, cannot update")

		    if args['name']:
			    result.name = args['name']
		    if args['views']:
			    result.views = args['views']
		    if args['likes']:
			    result.likes = args['likes']

		    db.session.commit()

		    return result

    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")

# api.add_resource(HelloWorld, "/helloworld/<string:name>")    # add class HelloWorld to the API, pass the name(string data type) to get request

if __name__ == "__main__":
    app.run(debug=True)   # only run "debug=True" on development environment (not recommended in production)