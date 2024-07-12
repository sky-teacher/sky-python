from colorama import init, Fore

# 初始化 colorama
init(autoreset=True)
# 定义打印带颜色文本的函数
def print_colored(text, color=Fore.WHITE):
    if isinstance(color, tuple):  # 检查 color 是否是元组
        color_str = ''.join(color)  # 将元组中的元素连接成一个字符串
        print(color_str + text)  # 连接颜色字符串和文本进行打印
    else:
        print(color + text)  # 如果 color 是字符串，直接连接颜色和文本进行打印

# 示例用法
#print_colored("红色文字", (Fore.RED,))
#print_colored("绿色文字", (Fore.GREEN,))
#print_colored("蓝色文字", (Fore.BLUE,))
#print_colored("黄色文字", (Fore.YELLOW,))