import os
from uuid import uuid4
path = os.path.join(str(os.path.abspath(os.path.basename(__file__))).replace('asd.py',''),"static\\uploads\\")
print(path)
'''
insert user(name,pwd,email,phone,info,face,uuid,addtime) values('猪','zhu','254573@qq.com','17851243564','我是一只猪','12','asdwasdwaca',now());
'''
count = 17851243564
cou = 254573
s=['鼠','牛','虎','兔','龙','蛇','马','羊','猴','鸡','狗','猪']
s1=['shu','niu','hu','tu','long','she','ma','yang','hou','ji','gou','zhu']
for i in range(0,12):
    print('insert user(name,pwd,email,phone,info,face,uuid,addtime) values(\''+s[i]+'\',\''+s1[i]+'\',\''+str(cou+i)+'@qq.com\',\''+str(count+i)+'\',\'我是一只'+s[i]+'\','+str(i+1)+',\''+str(uuid4())+'\',now());')


#
# insert into userlog(user_id,ip,addtime) values(29,'127.0.0.1',now());
# insert into userlog(user_id,ip,addtime) values(30,'127.0.0.2',now());
# insert into userlog(user_id,ip,addtime) values(31,'127.0.0.3',now());
# insert into userlog(user_id,ip,addtime) values(34,'127.0.0.4',now());
# insert into userlog(user_id,ip,addtime) values(33,'127.0.0.5',now());
# insert into userlog(user_id,ip,addtime) values(35,'127.0.0.6',now());
#
#
#
#
#








