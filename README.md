学习《推荐系统开发实战》一书，编写的各章节代码以及三个推荐系统的实现

## 各章节代码编写
## 三大案例
- 前端都是Vue，后端是django
- 安装node，使用node的npm安装vue、vue-cli、vue-router
- 对于每个案例使用的vue包在package.json中，通过npm install安装
- vue创建项目的时候，项目名称不能是骆驼命名法，都使用小写字母即可
### 搭建新闻推荐系统
- 虽然存在数据库备份，但我还是要从最出的步骤做起
- 在mysql中新建数据库newsrec，创建表：cate，news，newbrowse，newhot，newsim，newtag
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
- 运行python manage.py createsuperuser，创建django的后台管理账户

  #### 处理数据
- 原始数据是7个Excel文件
- 先整合下7个Excel文件中涉及到的新闻类别，插入到cate表
- 将原始Excel中，类别字段用数字替代，与cate表对应即可
- 通过navicat将增加字段后的excel文件导入mysql的news表中，一共7个文件
- 运行NewsKeyWordsSelect.py,基于TFIDF，对新闻关键词进行抽取
- 使用xlrd读取Excel文件，必须是xls格式的
- 运行NewsHotValueCal.py，计算新闻热度值，写入newhot表
- 运行NewsTagcCorres.py，根据新闻标签或者关键词，获取对应的新闻信息，写入newtag表
- 运行NewsCorrelationCalculation.py，计算新闻相关度，同时写入newsim表
- 运行python manage.py createsuperuser，创建django的后台管理账户(admin/9003)
  
  #### 实现思路
- 各大主题下的热度排序
- 每篇新闻的关键词抽取和展示
- 基于item的推荐
- 热度榜（注意覆盖度）
- 为你推荐（不同用户行为不同看到的为你推荐也不同，指定几个用户作为展示）

### 搭建音乐推荐系统
- 前端依然是vue，后端django 

- 在mysql中新建数据库newsrec，创建表：cate、playlist、playlisttosongs、playlisttotag、sing、singsim、singtag、
  song、songlysic、songsim、songtag、user、userbrowse、userplaylistrec、usersim、usersingrec、usersongrec、usertag、useruserrec
  
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
  
- 运行python manage.py createsuperuser，创建django的后台管理账户(admin/9003)
  
  #### 数据处理
  
  ##### 数据获取
  
- playlist_id_name_all.txt记录的歌单的信息，共1066首，这是程序的入口，所以这里需要有初始数据，直接从给的案例中拷贝过来

- 运行GetPlayListMess.py进行歌单信息类的处理。可能是目标网站的反爬出机制，一次性爬1000多首歌，会失败很多，后来就几首几首的做，这个也是在爬虫中比较麻烦的一件事
  
- 爬虫完毕后，获取创建者信息，保存到user_mess_all.txt，歌单信息保存到pl_mess_all.txt，歌单包含的歌曲信息保存到ids_all1.txt
  
- 所有关于id的信息都保存到ids_all.txt中，关于这些id是怎么来了，程序中没有体现，所以直接从给的案例中拷贝，初步考虑应该跟保存到ids_all1.txt中一样，直接通过爬虫获取然后保存的
  
- 运行GetSongMess.py，根据歌曲ID获取歌曲信息，歌词保存到songs_lysics_all.txt中，歌曲信息保存到songs_mess_all.txt中，失败的信息写入error_ids_1.txt中
  
- 运行GetSingMess.py，根据歌曲ID获取歌手信息，保存到sings_mess_all.txt，错误信息保存到sings_mess_error_1.txt。这个文件没有运行成功，因为在爬虫的时候失败了。直接适用案例中给的数据
  
- 
  
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
- 新建数据库bookrec，创建三个表结构：book，cate，history
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
- 运行python manage.py createsuperuser，创建django的后台管理账户(admin/9003)
- 运行python manage.py runserver启动后台管理，访问地址： `http://127.0.0.1:8000/admin`
- 运行model.py，对模型进行训练和保存
- 在BookRec-Vue下，运行`npm run dev`，启动前端vue，进行访问
  
  #### 数据处理
- 爬取某图书网站的数据，但原始数据没有提供，提供了处理后的数据“豆瓣图书.xlsx”，但实际中，还是要自己学会将原始数据进行转化和处理，毕竟原始数据不能作为推荐算法直接使用，需要挖掘和分析
- prepare.py将“豆瓣图书.xlsx”转换成可以直接导入数据库的txt文本格式（to_sql.txt）
- 利用navicat把to_sql.txt内容导入数据库的book表，需要给book表的name字段长度增加到200，否则导入时，有部分数据会因为长度问题而无法导入

  #### 实现思路
- 基于GBDT模型的图书推荐（不同用户行为不同看到的为你推荐也不同，指定几个用户作为展示）
- 图书详情展示
- 我的足迹