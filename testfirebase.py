import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://comp7940-8e8fa-default-rtdb.firebaseio.com/'
})
def add_post(researchname):
    # Get a database reference to our posts
    ref = db.reference('posts')
    # Check if the post with the same searchname exists
    posts_ref = db.reference('posts')
    posts_snapshot = posts_ref.get()
    if posts_snapshot:
        for post_key in posts_snapshot:
            post = posts_snapshot[post_key]
            if 'searchname' in post and post['searchname'] == '%s' % researchname:
                # Update the count value
                post_ref = db.reference('posts/' + post_key)
                post_ref.update({'count': post['count'] + 1})
                break
        else:
            # Push a new post to the database
            new_post_ref = ref.push()
            new_post_ref.set({
                'searchname': '%s' % researchname,
                'discribe': 'This is a test post.',
                'count': 1
            })
    else:
        # Push a new post to the database
        new_post_ref = ref.push()
        new_post_ref.set({
            'searchname':'%s' % researchname,
            'discribe': 'This is a test post.',
            'count': 1
        })
        

# Read the posts from the database
# posts_ref = db.reference('posts')
# posts_snapshot = posts_ref.get()
# if posts_snapshot:
#     for post_key in posts_snapshot:
#         post = posts_snapshot[post_key]
#         if 'searchname' in post:
#             print(post['searchname'])

#根据searchname value 找到对应的count value
def get_count(researchname):
    posts_ref = db.reference('posts')
    posts_snapshot = posts_ref.get()
    if posts_snapshot:
        for post_key in posts_snapshot:
            post = posts_snapshot[post_key]
            if 'searchname' in post and post['searchname'] == '%s' % researchname:
                return post['count']

# 根据searchname对应的count值返回经常搜索的前3个 searchname
def rankdatabase():
    posts_ref = db.reference('posts')
    posts_snapshot = posts_ref.get()

    # Dictionary to store the count for each searchname
    searchname_counts = {}

    if posts_snapshot:
        for post_key in posts_snapshot:
            post = posts_snapshot[post_key]
            if 'searchname' in post:
                searchname = post['searchname']
                if searchname in searchname_counts:
                    searchname_counts[searchname] += post['count']
                else:
                    searchname_counts[searchname] = post['count']

        # Sort the dictionary by count values in descending order
        sorted_counts = dict(sorted(searchname_counts.items(), key=lambda item: item[1], reverse=True))

        # Return the top 3 most frequently searched searchnames
        return list(sorted_counts.keys())[:3]

#print(rankdatabase())

# add_post("school")
# print(get_count("researchname"))

