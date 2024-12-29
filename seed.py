from app import app
from models import db, User, Post

with app.app_context():  
    db.drop_all()
    db.create_all()

    # USERS
    users = [
        User(first_name ="John", last_name = "Watson", image_url="https://i.pinimg.com/736x/62/9c/bc/629cbca02276c76a18da29667a07a26c.jpg"),
        User(first_name ="Sherlock", last_name = "Holmes", image_url="https://static.independent.co.uk/s3fs-public/thumbnails/image/2014/01/06/22/sherlock-bbc.jpg"),
        User(first_name ="Beyonce", last_name = "Knowles", image_url="https://static.wikia.nocookie.net/beyonce/images/2/2e/Beyonc%C3%A9.jpg/revision/latest?cb=20241210091706"),
        User(first_name ="Stuart", last_name = "Little", image_url="https://static.wikia.nocookie.net/sony-pictures-entertaiment/images/3/31/6745e028f4b0af4222ab5cc92648438b.png/revision/latest?cb=20190102203618"),
        User(first_name ="Amelia", last_name = "Bedelia", image_url="https://supadu-io.imgix.net/harpercollins-ameliabedelia/ameliabedelia-site/characters/young-amelia-large.jpg"),
        User(first_name ="Patrick", last_name = "Bateman", image_url="https://static.wikia.nocookie.net/villains/images/0/06/Patrick_Bateman_V.2.jpg/revision/latest/scale-to-width/360?cb=20240607224424")
    ]

    db.session.add_all(users)
    db.session.commit()

    # POSTS
    posts = [
        Post(title ='Hello', content="This is my first post", user_id=1),
        Post(title ='AAAAH!', content="I just sold out my first show", user_id=3),
        Post(title ='BOOO', content="New York City is no place for a mouse", user_id=4),
        Post(title ='yaaaayyy', content="I am better than everyone", user_id=6)
    ]

    db.session.add_all(posts)
    db.session.commit()



