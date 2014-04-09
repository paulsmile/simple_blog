一个使用Django和Bootstrap搭建起来的博客    
功能仍然相当不完善，待完善的时候我再修改这个README的内容吧:)    
    
###依赖：    
1、django-contrib-comments    
2、django-pagination   
3、pytz     

    
###目前已经实现的功能：    
1、博客正文支持markdown语法，支持代码高亮    
2、博客正文中的段落、图片代码等内容能够按照指定的顺序来显示    
3、支持评论功能    
4、首页实现了分页显示    
5、实现了RSS功能    

###目前存在的问题：   
1、模板中添加上国际化的支持，但是不起作用   
2、admin页面无法管理comment的内容，错误提示：Are time zone definitions and pytz installed? 这是因为mysql的mysql数据库中没有timezone表，尝试执行：mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql，但是提示一连串的Warning: Unable to load '/usr/share/zoneinfo/Asia/Riyadh87' as time zone. Skipping it.
对此问题查询过网上资料，网上资料反映这是Debian系的的一个bug。暂时没有解决办法。
   
