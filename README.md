学习《推荐系统开发实战》一书，编写的各章节代码以及三个推荐系统的实现

### 各章节代码编写

### 搭建新闻推荐系统
- 在mysql中新建数据库newsrec
- 导入数据库备份，原备份文件中，如果字段类型是datetime时，后面有长度，这样使用navicat导入会报错，需要把长度去掉，然后导入才不会报错
- 安装node，使用node的npm安装vue、vue-cli、vue-router
- vue创建项目的时候，项目名称不能是骆驼命名法，都使用小写字母即可
  
  #### 实现思路
- 各大主题下的热度排序
- 每篇新闻的关键词抽取和展示
- 基于item的推荐
- 热度榜（注意覆盖度）
- 为你推荐（不同用户行为不同看到的为你推荐也不同，指定几个用户作为展示）

### 搭建音乐推荐系统
- 在MySQL中新建数据库musicrec，这次数据太多，不再直接导入，由程序运行产生
- 前端依然是vue，后端django
  
  #### 实现思路
- 利用网易云API获取部分数据
- 基于标签进行歌单详情页的推荐、歌曲详情页的推荐、歌手详情页的推荐
- 基于用户的协同过滤算法给用户推荐用户、个用户推荐歌曲
- 基于物品的协同过滤算法给用户推荐歌手
- 基于内容的推荐算法给用户推荐歌单
- 个性化排行榜
- 为你推荐（不同用户行为不同看到的为你推荐也不同）
- 我的足迹，展示用户在站内的行为
### 图书推荐系统
- 前端依然是vue，后端django

- 新建数据库bookrec，导入三个表结构：book、cate、history

- 使用django作为后端，则首次需要运行python manage.py migrate，则会在数据库中创建django的表，我猜测django会根据models.py定义 的实体去处理
  - auth_group

  - auth_group_permissions  

  - auth_permission

  - auth_user

  - auth_user_groups

  - auth_user_user_permissions

  - django_admin_log

  - django_content_type

  - django_migrations

  - django_session
  
- 不同的django项目都会存在上面表，但每个项目自己使用的数据表，则是根据models.py中定义的class生成
  
- 爬取某图书网站的数据，但原始数据没有提供，提供了处理后的数据“豆瓣图书.xlsx”，但实际中，还是要自己学会将原始数据进行转化和处理，毕竟原始数据不能作为推荐算法直接使用，需要挖掘和分析

- prepare.py将“豆瓣图书.xlsx”转换成可以直接导入数据库的txt文本格式（to_sql.txt）

- 利用navicat把to_sql.txt内容导入数据库的book表，需要给book表的name字段长度增加到200，否则导入时，有部分数据会因为长度问题而无法导入

- 运行python manage.py createsuperuser，创建django的后台管理账户

- 运行python manage.py runserver启动后台管理，访问地址： `http://127.0.0.1:8000/admin`

- 运行model.py，对模型进行训练和保存

  #### 实现思路

- 基于GBDT模型的图书推荐（不同用户行为不同看到的为你推荐也不同，指定几个用户作为展示）

- 图书详情展示

- 我的足迹