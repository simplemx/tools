# 用途

将东方通服务器复制到多个目录下，并且修改相应的端口配置等。



# 使用方法

1. 修改config.py文件里的TongWebPath为待复制的东方通服务器目录

2. 修改config.py文件里的targetPath数组，每个元素为一个东方通服务器的配置

"path":"./TongWeb5.0_group",--东方通服务器地址

"http_port":"18093",--http服务端口，也就是待发布的应用http接口

"admin_port":"18094",--东方通管理后台端口

"iiop_port":"18095",--iiop端口，暂时没使用

"jmx_port":"18096"--jmx端口，暂时没使用

3. 修改完毕后，执行python deploy.py即可
