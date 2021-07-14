学习《推荐系统开发实战》一书，编写的各章节代码以及三个推荐系统的实现

## 各章节代码编写
## 三大案例
- 前端都是Vue，后端是django
- 安装node，使用node的npm安装vue、vue-cli、vue-router
- 对于每个案例使用的vue包在package.json中，通过npm install安装
- vue创建项目的时候，项目名称不能是骆驼命名法，都使用小写字母即可
### 搭建新闻推荐系统
- 虽然存在数据库备份，但我还是要从最初的步骤做起
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
- 运行python manage.py makemigrations news，让django存储models中的信息
- 运行python manage.py migrate，完成数据库表的创建：cate，news，newbrowse，newhot，newsim，newtag
- 运行python manage.py createsuperuser，创建django的后台管理账户(admin/9003)

  #### 处理数据
- 原始数据是7个Excel文件
- 先整合下7个Excel文件中涉及到的新闻类别，插入到cate表:
  ```
  1：国际要闻，2：互联网，3：经济要闻，4：中国军事，5：社会公益，6：书评，7：影视综艺
  ```
- 将原始Excel中，类别字段用数字替代，与cate表对应即可
- 通过navicat将增加字段后的excel文件导入mysql的news表中，一共7个文件
- 也可以将excel文件转成csv格式的进行导入，很多导入的工具支持csv而不支持excel
- 无论是excel格式还是csv格式，导入的时候注意字段需要对应起来  
- 导入的方法应该是自己写一套最好了（暂未实现）  
- 运行NewsKeyWordsSelect.py,基于TFIDF，对新闻关键词进行抽取
- 使用xlrd读取Excel文件，必须是xls格式的
- 运行NewsHotValueCal.py，计算新闻热度值，写入newhot表
- 运行NewsTagcCorres.py，根据新闻标签或者关键词，获取对应的新闻信息，写入newtag表
- 运行NewsCorrelationCalculation.py，计算新闻相关度，同时写入newsim表
  
  #### 实现思路
- 各大主题下的热度排序
- 每篇新闻的关键词抽取和展示
- 基于item的推荐
- 热度榜（注意覆盖度）
- 为你推荐（不同用户行为不同看到的为你推荐也不同，指定几个用户作为展示）

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
  
- 所有关于id的信息都保存到ids_all.txt中，这里面就是歌单id和其对应的歌曲id。关于这些id是怎么来了，程序中没有体现，所以直接从给的案例中拷贝，初步考虑应该跟保存到ids_all1.txt中一样，直接通过爬虫获取然后保存的
  
- 运行GetSongMess.py，根据歌曲ID获取歌曲信息，歌词保存到songs_lysics_all.txt中，歌曲信息保存到songs_mess_all.txt中，失败的信息写入error_ids_1.txt中
  
- 运行GetSingMess.py，根据歌曲ID获取歌手信息，保存到sings_mess_all.txt，错误信息保存到sings_mess_error_1.txt。这个文件没有运行成功，因为在爬虫的时候失败了。直接适用案例中给的数据
  
  ##### 数据导入
  
  由于这个项目的数据量比较打，所以数据导入是分开进行的
  
- 导入歌曲信息

  - 运行ToMySQL.py，执行song_mess_to_mysql方法，读取songs_mess_all.txt，将歌曲信息写入song表中。
  - 一共写入24343条记录。出错记录数是1609条。
  - 如果song_publish_time是null的，将信息记录到error_songs.txt，
  - 如果一行的内容长度分割后不是9，不再打印，直接记录到error_songs.txt
  - 修改song表的song_name和song_sing_id字段长度到200，同时需要修改models.py下的song类

- 导入歌词信息

  - 运行ToMySQL.py，执行song_lysic_to_mysql方法，读取songs_lysics_all.txt，将歌词信息写入songlysic表中。
  - 错误信息写入error_lysic.txt。
  - 一共导入25952条记录，出错记录数是0

- 导入歌手信息

  - 运行ToMySQL.py，执行sing_mess_to_mysql方法，读取sings_mess_all.txt，将歌词信息写入sing表中。
  - 错误信息写入error_sings.txt。
  - 一共导入11637条记录，出错记录数是23条。
  - 保存歌手信息的文件sings_mess_all.txt中有 17555条记录，但存在重复记录，程序根据歌手id判断，避免重复导入
  - 如果一行的内容长度分割后不是6，不再打印，直接记录到error_sings.txt

- 导入用户信息

  - 运行ToMySQL.py，执行user_mess_to_mysql方法，读取user_mess_all.txt，将歌词信息写入user表中。
  - 错误信息写入error_users.txt中，包括生日是空或者等于null字符串、一行内容分割后长度小于14的
  - 一共导入643条记录，出错记录数是158条

- 导入歌单信息

  - 运行ToMySQL.py，执行playlist_mess_to_mysql方法，读取pl_mess_all.txt，将歌词信息写入playlist表中。
  - 错误信息写入error_playlist.txt中，包括歌单创建时间是空或者等于null字符串、创建者 id不在user表中的
  - 一共导入877条记录，出错记录数是189条

- 导入歌单和歌曲的id对应关系

  - 运行ToMySQL.py，执行playlist_sing_mess_to_mysql方法，读取ids_all.txt，将歌单和歌曲对应关系写入playlisttosongs表中。
  - 错误信息写入error_playlist_sing.txt中，记录错误的歌单id和歌曲id
  - 共计37651条记录，其中包含1066个歌单，每个歌单下包含若干歌曲，在不同的歌单下，会包含重复的歌曲

- 导入歌单和歌单标签对应关系

  - 运行ToMySQL.py，执行playlist_tag_mess_to_mysql方法，读取pl_mess_all.txt，将歌单和歌单标签对应关系写入playlisttotag表中
  - 错误信息写入error_playlist_tag.txt中
  - 共有1066个歌单，导入的数据量是2846，因为一个歌单存在多个标签

- 处理歌手和歌曲的关系

- 导入用户和标签的对应关系

  - 直接读取数据库的playlist表，然后获取用户id和tag写入usertag表中，共写入2377条数据
  - 错误信息写入error_user_tag.txt中

- 在导入过程中，可能会因为出错，重新导入，但数据量这么大，每次导入不应该先清空数据库的数据再导入，应该支持追加导入，自动判断是否重复等

  #### 实现思路

- 利用网易云API获取部分数据

- 基于标签进行歌单详情页的推荐、歌曲详情页的推荐、歌手详情页的推荐

- 基于用户的协同过滤算法给用户推荐用户、个用户推荐歌曲

- 基于物品的协同过滤算法给用户推荐歌手

- 基于内容的推荐算法给用户推荐歌单

- 个性化排行榜

- 为你推荐（不同用户行为不同看到的为你推荐也不同）

- 我的足迹，展示用户在站内的行为
