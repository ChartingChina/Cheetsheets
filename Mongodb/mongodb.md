# Mongo数据库基本操作



## 1. 安装Mongo数据库

官方网站下载msi文件，运行安装

../bin添加到path



## 2. 运行MongoDB

```
# 运行服务器
mongod

# 运行客户端
mongo
```



## 3. MongoDB操作

参考官方文档：

- [MongoDB CRUD Operations](https://docs.mongodb.com/manual/crud/)

- [mongo Shell Methods](https://docs.mongodb.com/manual/reference/method/)



### 3.1 创建和删除表

```
# 显示数据库列表
> show dbs

# 使用数据库
> use dbname

# 显示数据库中的集合（或者表，一个意思）
> show collections/show tables

# 创建集合
> db.createCollection('collection')

# 删除集合
> db.collection.drop()
```



### 3.2 CRUD

#### Insert

```
# 插入文档
> db.collection.insert(document)

# 插入多个文档
> db.collection.insert([list of documents])
```

#### Find

```
# 列出所有文档
> db.collection.find()

# 条件查询
> db.collection.find({query})
```

#### Remove

```
# 删除符合条件的文档
> db.collection.remove({query})

# 删除全部文档
> db.collection.remove({})
```

#### Update

```
# 完全替换文档
> db.collection.update({query}, {update})

# 部分修改文档
> db.collection.update({query}, {$set:{update}})
```



### 3.3 高级查询

#### where

传递函数

```
> db.collection.find({$where: function(){return this...}})
```

#### limit, skip

```
> db.collection.find({query}).limit(number).skip(number)
```

#### project

值显示部分fields

```
> db.collection.find({query}, {_id:0, field:1, ...})
```

#### sort

```
# 升序
> db.collection.find({query}).sort({field:1})

# 降序
> db.collection.find({query}).sort({field:-1})
```

#### count

```
> db.collection.find({query}).count()
# 或者
> db.collection.count({query})
```

#### distinct

```
> db.collection(field, {query})
```



### 3.4 Aggregate

```
# count
db.orders.aggregate([
   {$match: {query}},
   {$group: {_id: "$field to group", 
   			 count: {$sum: 1}}}
])

# sum
db.orders.aggregate([
   {$match: {query}},
   {$group: {_id: "$field to group", 
   			 total: {$sum: "$field to sum"}}}
])
```

### 3.5 Pipeline

```
# $match | $group | $sort

db.collection.aggregate(
	{$match: {}},
	{$group: {}},
	{$sort: {}},
)
```

#### Operations

- $group
- $match
- $sort
- $limit
- $skip
- $unwind

##### $unwind

```
db.collection.aggregate([
	{$unwind:{
		path:'$field', 
		preserveNullAndEmptyArrays:true}}
])
```

#### Expression

- $sum
- $avg
- $min
- $max
- $first
- $last
- $push

##### $push

```
# full list of values
db.orders.aggregate([
   {$match: {query}},
   {$group: {_id: "$field to group", 
   			 values: {$push: "$field to sum"}}}
])

# full list of documents
db.orders.aggregate([
   {$match: {query}},
   {$group: {_id: "$field to group", 
   			 documents: {$push: "$$ROOT"}}}
])
```

### 3.6 Index

```
# 创建索引
db.collection.ensureIndex({'field':1})

# 查询统计
db.collection.find({query}).explain('executionStats')
```



```
# 唯一索引
db.collection.ensureIndex({field:1}, {unique:true})

# 唯一索引
db.collection.ensureIndex({field1:1, field2:1})
```



```
# 查询索引
db.c2.getIndexes()

# 删除索引
db.c2.dropIndexes()
```



## 4. PyMongo

pip install pymongo

具体使用参见：[PyMongo文档](https://pymongo.readthedocs.io/en/stable/)

```python
from mongodb import MongoClient

# 连接MongoDB
client = MongoClient('mongodb://localhost:27017')

# 列出所有数据库
client.list_databases()

# 获取数据库
db = client.database_name

# 或者用字典方式获取（如果包含非名称字符）
db = client['database_name']

# 列出所有collection
db.list_collections()
```



## 5. MongoEngine

pip install mongoengine

具体使用参见：[MongoEngin文档](http://docs.mongoengine.org/)



### 5.1 [Connecting](https://docs.mongoengine.org/guide/connecting.html)

```python
from mongoengine import connect

# 不需要 conn = connect()
connect(db='database_name')

# 默认参数（可省缺）：host='localhost', port=27017
# 其他参数: username, password, authentication_source='admin'

# 默认：alias='default'
connect(db='database_name', alais='some_name')
```



```
disconnect('database_name')

# disconnect all
disconnect()
```



### 5.2 CRUD

#### Insert

```python
from mongoengine import Document, StringField, EmailField

class User(Document):
    email = EmailField(required=True)
    name = StringField(max_length=50)
    
user = User(email='test@email.com')
user.name = 'UserName'
user.save()
```

#### Update

```python
user = User.objects(email='test@email.com')
user.update(name='NewName')
```



更新多个field

```python
from mongoengine import Document, StringField, EmailField, IntField

class User(Document):
    name = StringField(max_length=50)
    email = EmailField(required=True, unique=True)
    age = IntField()

user = User.objects(email='test@email.com')
fields = {
    'name': 'NewName2',
    'age': 20
}
user.update(**fields)
```



### 5.3 EmbeddedDocument

```python
POST_STATUS = ('pending', 'published', 'deleted', 'draft')


class PostMetatag(EmbeddedDocument):
    title = StringField()
    description = StringField()
    encoding = StringField(default='utf-8')


class PostCategory(EmbeddedDocument):
    id = ObjectIdField()
    title = StringField()


class Posts(Document):
    title = StringField()
    metatag = DictField(EmbeddedDocumentField(PostMetatag))
    categorys = ListField(EmbeddedDocumentField(PostCategory))
    authors = ListField(ObjectIdField())
    status = StringField(choice=POST_STATUS)
```



```python
metatag = PostMetatag()
metatag.title = 'meta title'
metatag.description = 'meta description'

post = Post()
post.title = 'post title'
post.meta = metatag
post.status = 'pending'

```

