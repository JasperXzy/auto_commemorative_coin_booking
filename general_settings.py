from selenium.webdriver.chrome.service import Service as Service_Chrome
from selenium.webdriver.edge.service import Service as Service_Edge

# 驱动路径
path_chrome = Service_Chrome("./driver/chromedriver.exe")
path_edge = Service_Edge("./driver/msedgedriver.exe")

# 预约链接
booking_url = "https://eapply.abchina.com/coin/Coin/CoinIssuesDistribution?typeid=202301"

# 预约界面 Xpath
welcome_page_xpath = '/html/body/div[5]/div[2]/table/tbody/tr[5]/td[4]/input[1]'

# 数据库信息
host = ""  # 主机名
port =   # 端口
user = ""  # 账户
password = ""  # 密码
database = ""  # 信息所在数据库
table = ""  # 信息所在表

# 预约地址
place_arr = ['', '', '', 4]  # 分别为 [省行, 分行, 支行, 默认营业厅序号]

# 兑换时间
coindate = '2023-1-18'

# 短信验证码剪裁范围
y_0 = 1550
y_1 = 1620
x_0 = 125
x_1 = 345

# 总进程数
threads = 5


