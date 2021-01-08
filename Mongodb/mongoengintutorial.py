from mongoengine import connect, disconnect
from mongoengine import (Document, StringField, EmailField, IntField,
                         DictField, ListField, DateTimeField,
                         ObjectIdField,
                         EmbeddedDocument, EmbeddedDocumentField)


connect('test')

POST_STATUS = ('pending', 'published', 'deleted', 'draft')


class User(Document):
    name = StringField(max_length=50)
    email = EmailField(required=True, unique=True)
    age = IntField()


class PostMetatag(EmbeddedDocument):
    title = StringField()
    description = StringField()
    encoding = StringField(default='utf-8')


class PostCategory(EmbeddedDocument):
    id = ObjectIdField()
    title = StringField()


class Posts(Document):
    title = StringField()
    url = StringField()
    content = StringField()
    metatag = EmbeddedDocumentField(PostMetatag)
    categories = ListField(EmbeddedDocumentField(PostCategory))
    authors = ListField()
    status = StringField()
    updated_at = DateTimeField()
    created_at = DateTimeField()

    meta = {
        'auto_created_index': True,
        'index_background': True,
        'indexes': [{
            'name': 'status',
            'fields': ('status', 'created_at'),
        }, {
            'name': 'url',
            'fields': ('url', ),
            'unique': True
        }]
    }


# user = User(email='test2@email.com')
# user.name = 'test2'
# user.save()

# user = User.objects(email='test@email.com')
# user.update(age=16)

# user = User.objects(email='test2@email.com')
# fields = {
#     'name': 'test2newname',
#     'age': 20
# }
# user.update(**fields)

# user = User.objects(email='test2@email.com')
# user.update(name='testnewname', age=18)

post_metatag = PostMetatag()
post_metatag.title = 'meta title'
post_metatag.description = 'meta description'

post = Posts()
post.title = 'Hello world'
post.url = 'hello-world-4'
post.content = 'What a wonderful world'
post.metatag = post_metatag

post_category = PostCategory()
post_category.title = 'category title'
post.categories.append(post_category)

post.status = 'pending'
post.save()
