## attention
1. get_stocks 为爬取数据的代码
	- main 方法为程序入口
	- main 方法中的下发参数，比如说mysql_info 是作者的mysql连接信息，如果需要连接自己的数据库，需要修改mysql的配置信息；
	- main 方法中获取所有历史数据的代码为 ```mysql_obj.mysql_input_all_stock_data(stocks_code_df, method='replace')```，笔者因为已经获取，所以注释掉了；获取当天的数据的代码为```mysql_obj.mysql_input_all_stock_data(stocks_code_df, method='append')``` ，每天都需要运行。
	- 每日的日志均在log文件夹下可以看到。
2. 关于自动运行，笔者写了一个 .bat 脚本，并且在windows任务管理中设置每日执行；然后提供了脚本文件 schedule._run.py脚本文件，可以定时运行；这两种方法均可以，由于作者经常关机，所以选择了第一种。
3. code.ipynb 为简单的聚合分析。