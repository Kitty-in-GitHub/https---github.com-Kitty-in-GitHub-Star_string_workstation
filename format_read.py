import pandas as pd
import random
from datetime import datetime
import os
from typing import List, Union, Tuple

# 分割线
DEVIDE_LINE = '###########################'

# 三张表格的路径
WORKER_LIST_FILE_PATH = '1号表干员信息表.csv'
WORK_FLOW_FILE_PATH= '2号表工作流记录表.csv'
WORK_TO_BE_DONE_LIST_FILE_PATH = '3号待完成工作表.csv'

# 存放你们社团的工作分工类型
work_type_list = ['线下工作', '设计工作', '行政工作', '采购工作', '策划工作', 
                 '内建内训', '外联工作', '玉衡特别行动组', '星弦游戏工作室']

# 干员信息表和待完成工作表用到的常量
WORKER_LIST_WORKER_NUMBER = 'QQ号'
WORKER_LIST_PHONE_NUMBER='手机号'
WORKER_LIST_WORK_COUNT = '已经从事过的工作数量'
ROW_NAME_WORKER_NAME = '干员昵称'
WORK_ID = '工作流水号'
WORK_DESCRIBE = '工作描述'
WORK_ASSIGN_TIME='工作日期'

# 待完成工作表常量
WTBDL_WORK_ID = '待完成工作序号'
WTBDL_WORK_DESCRIBE = '工作描述'
WTBDL_ASSIGN_TIME = '工作注册时间'
WTBDL_WORK_TYPE = '工作类型'

# 表头名称
WORKER_LIST_COLUMN_NAME=[WORKER_LIST_WORKER_NUMBER] + work_type_list + [WORKER_LIST_PHONE_NUMBER,ROW_NAME_WORKER_NAME,WORKER_LIST_WORK_COUNT]
WORK_FLOW_COLUMN_NAME=[WORKER_LIST_WORKER_NUMBER,ROW_NAME_WORKER_NAME,WORK_ID,WORK_DESCRIBE,WORK_ASSIGN_TIME]
WORK_TO_BE_DONE_LIST_COLUMN_NAME=[WTBDL_WORK_ID,WTBDL_WORK_DESCRIBE,WTBDL_ASSIGN_TIME,WTBDL_WORK_TYPE]

###############################################
############    表格操作    ###############
###############################################
# 一次性加载三张表格
def load_tables():
    """
    Returns:
        operator_df:干员名单
        workflow_df:工作记录表
        work_to_be_done_list_file_path:待完成工作表
    """
    try:
        operator_df = pd.read_csv(WORKER_LIST_FILE_PATH)
        workflow_df = pd.read_csv(WORK_FLOW_FILE_PATH)
        work_to_be_done_list = pd.read_csv(WORK_TO_BE_DONE_LIST_FILE_PATH)
        return operator_df, workflow_df ,work_to_be_done_list
    except FileNotFoundError:
        print("错误：未找到数据文件，请确保三张表存在")
        exit()

# 保存员工工作表和工作记录表
def save_tables(operator_df, workflow_df):
    """
    """
    operator_df.to_csv(WORKER_LIST_FILE_PATH, index=False)
    workflow_df.to_csv(WORK_FLOW_FILE_PATH, index=False)

# 保存待完成工作标
def save_to_be_done_list(work_to_be_done_list):
    """
    """
    work_to_be_done_list.to_csv(WORK_TO_BE_DONE_LIST_FILE_PATH, index=False)

# 检查表格是否存在，根据文件缺少的情况返回值
def weather_tables_exsit()-> bool:
    """
    Returns:
        file_exsit_flag:当文件齐全时返回0，缺少工作

    """
    file_exsit_flag=True

    # 依次检查三张表
    file_path=WORKER_LIST_FILE_PATH
    if os.path.exists(file_path):
        print(f"\n文件 '{file_path}' 已经存在")
    else:
        print(f"\n文件 '{file_path}' 不存在")
        file_exsit_flag=False

    file_path=WORK_FLOW_FILE_PATH
    if os.path.exists(file_path):
        print(f"\n文件 '{file_path}' 已经存在")
    else:
        print(f"\n文件 '{file_path}' 不存在")
        file_exsit_flag=False

    file_path=WORK_TO_BE_DONE_LIST_FILE_PATH
    if os.path.exists(file_path):
        print(f"\n文件 '{file_path}' 已经存在")
    else:
        print(f"\n文件 '{file_path}' 不存在")
        file_exsit_flag=False

    # 返回检查结果
    return file_exsit_flag

# 检查表格是否存在以及表头是否正确。如果表格存在且表头符合要求返回True，否则返回False
def tables_column_name_check(table_to_be_check_file_path:str,column_name:List[str])->bool:
    """
    Parameter:
        table_to_be_check_file_path:需要检查的文件路径
        column_name:表头内容
    """
    # 检查表格是否存在
    try:
        table_to_be_check=pd.read_csv(table_to_be_check_file_path)
    except FileNotFoundError:
        print(f"错误：未在 {table_to_be_check_file_path} 找到对应文件")
        return False
    
    # 检查表头长度
    headers = table_to_be_check.columns.tolist()
    if(len(headers)!=len(column_name)):
        print(f"路径为 {table_to_be_check_file_path} 的表格表头的长度与程序设定的表头长度不一致，程序设定的表格长度为{len(column_name)}")
        print(f"表格头应该为{column_name}")
        print(f"而现有文件的表格头为{headers}")
        return False

    # 遍历表头名称列表，取出csv表格的表头逐个对比
    for index, name in enumerate(column_name):
        if(name!=headers[index]):
            print(f"位于{table_to_be_check_file_path}的表格头内容与程序设定的不一致")
            print(f"文件中的表格头为{name}")
            print(f"程序期望的表格头为{headers[index]}")
            return False
    return True

# 表格初始化
def csv_init():
    """
    逐张表检查文件是否存在，以及表头是否正确
        - 存在且表头正确 - 检查下一张表
        - 有表格不存在或表头错误 - 询问是否创建缺失和错误的表格
    """
    print("工具初始化中")
    # 储存需要重建的表格
    rebuild_table_name=[]
    # 检查干员信息表
    if tables_column_name_check(WORKER_LIST_FILE_PATH,WORKER_LIST_COLUMN_NAME):
        print("干员信息表检查通过")
    else:
        print("干员信息表不存在或表头错误")
        rebuild_table_name+=['干员信息表']
    
    # 检查工作记录表
    if tables_column_name_check(WORK_FLOW_FILE_PATH,WORK_FLOW_COLUMN_NAME):
        print("工作记录表检查通过")
    else:
        print("工作记录表不存在或表头错误")
        rebuild_table_name+=['工作记录表']

    # 检查待完成工作表
    if tables_column_name_check(WORK_TO_BE_DONE_LIST_FILE_PATH,WORK_TO_BE_DONE_LIST_COLUMN_NAME):
        print("待完成工作表检查通过")
    else:
        print("待完成工作表不存在或表头错误")
        rebuild_table_name+=['待完成工作表']

    # 判断是否需要重新建立表格
    if(len(rebuild_table_name)==0):
        print("\n所有的csv文件均存在，且表头正确")
    else:
        print(f"\n需要创建或重新创建的文件为{rebuild_table_name}，请问是否要进行自动重建")
        print("若是，程序将创建并覆盖出错和缺失的文件；若否，程序将退出，您需要手动改正或创建文件")
        print("请问是否进行自动重建(y/n)")
        if ask_for_yes_or_no():
            # 执行重建
            if('干员信息表' in rebuild_table_name):
                rebuild_csv(WORKER_LIST_FILE_PATH,WORKER_LIST_COLUMN_NAME)
            if('工作记录表' in rebuild_table_name):
                rebuild_csv(WORK_FLOW_FILE_PATH,WORK_FLOW_COLUMN_NAME)
            if('待完成工作表' in rebuild_table_name):
                rebuild_csv(WORK_TO_BE_DONE_LIST_FILE_PATH,WORK_TO_BE_DONE_LIST_COLUMN_NAME)
            return
        else:
            exit()
    return

# 根据给定的文件路径和表头创建CSV文件（覆盖已存在的文件）
def rebuild_csv(file_path: str, column_name: Union[List[str], tuple]) -> bool:
    """
    根据给定的文件路径和表头创建CSV文件（覆盖已存在的文件）

    Parameters:
        file_path (str): 要创建的CSV文件路径（如：'data/output.csv'）
        column_name (List[str] or tuple): 表头（列名）列表或元组
        
    Returns:
        bool: 创建成功返回True，失败返回False
        
    Examples:
        >>> rebuild_csv('data.csv', ['姓名', '年龄', '城市'])
        True
        >>> rebuild_csv('data.csv', ('ID', 'Name', 'Score'))
        True
    """
    try:
        # 检查column_name是否为列表或元组
        if not isinstance(column_name, (list, tuple)):
            raise TypeError("column_name必须是列表或元组")
            
        # 检查表头元素是否都是字符串
        if not all(isinstance(name, str) for name in column_name):
            raise TypeError("所有表头元素必须是字符串")
        
        # 创建空的DataFrame并指定列名
        df = pd.DataFrame(columns=column_name)
        
        # 写入CSV文件
        df.to_csv(file_path, index=False, encoding='utf-8')

        return True
        
    except Exception as e:
        print(f"创建CSV文件失败: {str(e)}")
        return False
#############################################
###########     工具函数    ###################
###############################################
# 索要数字
def ask_for_number(min: int, max: int, question: str = '请输入范围内的数字') -> int:
    """
    持续要求用户输入，直到获得指定范围内的整数
    
    Parameters:
        min (int): 允许的最小值
        max (int): 允许的最大值
        question (str): 提示用户输入的文本
        
    Returns:
        str: 用户输入的合法数字
        
    Raises:
        ValueError: 如果min > max时会抛出异常
    """
    if min > max:
        raise ValueError(f"最小值{min}不能大于最大值{max}")

    while True:
        try:
            number_input = int(input(f"{question} ({min}-{max}): ").strip())

            if min <= int(number_input) <= max:
                return number_input
            else:
                print(f"输入必须在{min}到{max}之间")
        except ValueError:
            print(f"请输入有效的整数，而您的输入值是 {number_input}")

# 循环要求用户输入（y/n），输入Y、y返回True，输入N、n返回False，否则无法结束函数
def ask_for_yes_or_no(question='请输入y或n')->bool:
    """
    Return:
        输入Y、y返回True，输入N、n返回False，否则无法结束函数
    """
    while True:
        confirm=input(question)
        if confirm in ['y','Y']:
            return True
        elif confirm in ['n','N']:
            return False
        else :
            print(f"\n输入无效，{question}”")

# 自动随机分配工作，获取被抽中人的相关信息
def assign_work(operator_df:pd.DataFrame, work_type:pd.DataFrame):
    """
    Returns:
        selected_operator[WORKER_LIST_WORKER_NUMBER]:被分配到工作的人员工号（这里用的是qq号）
        selected_operator[ROW_NAME_WORKER_NAME]:被分配到工作的人员姓名
    """
    preferred_operators = operator_df[operator_df[work_type_list[work_type-1]] == 1]
    
    if preferred_operators.empty:
        print(f"没有干员倾向于从事工作类型{work_type_list[work_type-1]}")
        return None, None
    
    min_work_count = preferred_operators[WORKER_LIST_WORK_COUNT].min()
    candidates = preferred_operators[preferred_operators[WORKER_LIST_WORK_COUNT] == min_work_count]
    
    selected_operator = candidates.sample(1).iloc[0]
    return selected_operator[WORKER_LIST_WORKER_NUMBER], selected_operator[ROW_NAME_WORKER_NAME]

# 索要工作类型
def ask_for_work_type(work_types:List[str])->str:
    """
    Parameter:
        work_types : 工作类型列表，需要是一个字符串列表
    Return:
        work_type_choosen : 选中工作类型的序号，如果选择强制退出，则返回q
    """
    while True:
        # 打印工作类型
        for i in range(len(work_types)):
            print(f"{i}. {work_types[i]}")

        # 获取序号
        work_type_choosen = input("请输入工作类型的序号，或输入q返回")
        
        # 强制退出
        if work_type_choosen == 'q':
            break

        # 校验工作序号
        if not work_type_choosen.isdigit() or int(work_type_choosen) < 0 or int(work_type_choosen) > (len(work_types)-1):
            print("输入错误：请输入工作类型的序号，或输入q返回")
            continue
        else:
            break

    return work_type_choosen

# 向某个表格中添加信息，根据是否成功返回添加数据后的pd.datafram，布尔值标签，只检查是否符合表头长度
def add_information_to_a_format(selected_df: pd.DataFrame, added_information: List[str]) -> Tuple[pd.DataFrame, bool]:
    """
    向DataFrame中添加新记录，仅检查数据长度是否匹配表头
    
    Parameters:
        selected_df: 选中的表格
        added_information: 需要添加进表格的数据（列表形式）
        
    Returns:
        Tuple[pd.DataFrame, bool]: 
            - 添加成功: 返回(新DataFrame, True)
            - 添加失败: 返回(原DataFrame, False)
            
    Example:
        >>> df = pd.DataFrame(columns=['Name', 'Age'])
        >>> new_df, success = add_information_to_a_format(df, ['John', '25'])
    """
    # 获取表头信息
    headers_list = selected_df.columns.tolist()
    
    # 比较表头长度和添加信息的列表长度
    if len(headers_list) == len(added_information):
        # 创建新记录（字典形式）
        new_record = {col: [val] for col, val in zip(headers_list, added_information)}
        
        # 将新记录转换为DataFrame并合并
        new_record_df = pd.DataFrame(new_record)
        return_df = pd.concat([selected_df, new_record_df], ignore_index=True)
        
        return return_df, True
    else:
        # 长度不匹配时返回原DataFrame
        print("Error: 您想向表格中添加的信息长度和表头长度不等！")
        print(f"表头长度: {len(headers_list)} (内容: {headers_list})")
        print(f"数据长度: {len(added_information)} (内容: {added_information})")
        return selected_df, False
###############################################
##########    手动操作  ##########
###############################################
# 手动删除工作记录
def delete_work_record(operator_df, workflow_df):
    print("\n当前所有工作记录:")
    print(workflow_df[[WORK_ID, ROW_NAME_WORKER_NAME, WORK_DESCRIBE, WORK_ASSIGN_TIME]])
    
    while True:
        record_id = input("\n请输入要删除的工作流水号(输入q返回主菜单): ")
        if record_id.lower() == 'q':
            return operator_df, workflow_df, False
        
        if not record_id.isdigit():
            print("错误：请输入数字流水号")
            continue
            
        record_id = int(record_id)
        if record_id not in workflow_df[WORK_ID].values:
            print(f"错误：流水号{record_id}不存在")
            continue
            
        break
    
    record = workflow_df[workflow_df[WORK_ID] == record_id].iloc[0]
    print(f"\n将要删除以下记录:")
    print(record)
    confirm = input("确认删除吗？(y/n): ").lower()
    if confirm != 'y':
        return operator_df, workflow_df, False
    
    qq = record[WORKER_LIST_WORKER_NUMBER]
    operator_df.loc[operator_df[WORKER_LIST_WORKER_NUMBER] == qq, WORKER_LIST_WORK_COUNT] -= 1
    workflow_df = workflow_df[workflow_df[WORK_ID] != record_id]
    
    return operator_df, workflow_df, True

# 手动导入工作记录
def manual_import_work(operator_df:pd.DataFrame, workflow_df:pd.DataFrame):
    """
    手动导入工作记录
    
    :param operator_df: 干员名单
    :param workflow_df: 工作流记录表
    """
    print("\n当前所有干员列表:")
    # 显示带索引的干员列表
    for idx, row in operator_df.iterrows():
        print(f"{idx}. QQ号: {row[WORKER_LIST_WORKER_NUMBER]}, 昵称: {row[ROW_NAME_WORKER_NAME]}, 工作总数: {row[WORKER_LIST_WORK_COUNT]}")
    
    while True:
        worker_idx = input("\n请输入干员编号(输入q退出): ")
        if worker_idx.lower() == 'q':
            print("用户手动取消")
            return operator_df, workflow_df
        
        try:
            worker_idx = int(worker_idx)
            if worker_idx < 0 or worker_idx >= len(operator_df):
                print(f"错误：编号必须在0-{len(operator_df)-1}范围内")
                continue
        except ValueError:
            print("错误：请输入有效的数字编号")
            continue
            
        # 获取选中的干员信息
        selected_worker = operator_df.iloc[worker_idx]
        qq = selected_worker[WORKER_LIST_WORKER_NUMBER]
        nickname = selected_worker[ROW_NAME_WORKER_NAME]
        
        # 生成新的工作流水号
        if not workflow_df.empty:
            new_id = workflow_df[WORK_ID].max() + 1
        else:
            new_id = 0
        
        # 创建工作记录
        print(f"您选中的干员是：{nickname}")
        description = input("请输入工作内容描述: ")
        work_date = datetime.now().strftime('%Y-%m-%d') + ' (手动导入)'
        
        new_record = {
            'QQ号': qq,
            '干员昵称': nickname,
            '工作流水号': new_id,
            '工作描述': description,
            '工作日期': work_date
        }
        
        # 更新数据
        workflow_df = workflow_df._append(new_record, ignore_index=True)
        operator_df.loc[operator_df[WORKER_LIST_WORKER_NUMBER] == qq, WORKER_LIST_WORK_COUNT] += 1
        save_tables(operator_df,workflow_df)
        
        return operator_df, workflow_df

# 手动向待完成工作表中填写一个新工作
def add_a_new_work(work_to_be_done_list):

    # 获取工作类型
    print("请选择工作类型")
    work_type = ask_for_work_type(work_type_list)

    # 如果工作类型标签为"q"则中断
    if work_type == 'q':
        return work_to_be_done_list

    # 生成新的工作流水号
    if not work_to_be_done_list.empty:
        new_id = work_to_be_done_list[WTBDL_WORK_ID].max() + 1
    else:
        new_id = 0
    
    # 索要工作描述
    work_descripution = input("请输入工作描述：")

    # 获取工作注册时间
    assign_time = datetime.now().strftime('%Y-%m-%d')

    # 创建工作记录
    new_record = {
        WTBDL_WORK_ID : new_id,
        WTBDL_WORK_DESCRIBE : work_descripution,
        WTBDL_ASSIGN_TIME :assign_time,
        WTBDL_WORK_TYPE : work_type
    }

    # 更新数据
    work_to_be_done_list= work_to_be_done_list._append(new_record, ignore_index=True)
    save_to_be_done_list(work_to_be_done_list)
    return work_to_be_done_list

# 从待完成工作表中选择工作并指派人员完成
def manual_assign_work_from_to_be_done(
        operator_df:pd.DataFrame,#干员信息表
        workflow_df:pd.DataFrame,#工作记录表
        work_to_be_done_list:pd.DataFrame#待完成工作表
        )->Union[pd.DataFrame,pd.DataFrame,pd.DataFrame,bool]:
    """
    从待完成工作表中手动选择工作并指派人员完成
    
    Parameters:
        operator_df：干员信息表
        workflow_df：工作记录表
        work_to_be_done_list：待完成工作表
        
    Returns:
        operator_df：更新后的干员信息表
        workflow_df：更新后的工作记录表
        work_to_be_done_list：更新后的待完成工作表
        Flag：标志位，标志是否用户中断了
    """
    # return operator_df, workflow_df, work_to_be_done_list, False
    if len(work_to_be_done_list)<1:
        print("待完成工作表为空，请您先向待完成工作表中填写工作再通过本选项进行分配")
        return operator_df,workflow_df,work_to_be_done_list,False
    
    # 显示待完成工作表
    view_work_to_be_done_list(work_to_be_done_list)
    print("以上是我们所有等待分配的工作")

    # 获取要分配的工作序号
    work_about_to_be_done_ID = ask_for_number(0,len(work_to_be_done_list)-1,"请输入您要分配的待完成工作序号")

    # 获取待分配的工作的相关信息
    selected_work = work_to_be_done_list[work_to_be_done_list[WTBDL_WORK_ID] == work_about_to_be_done_ID].iloc[0]
    
    # work_type = selected_work['工作类型']
    description = selected_work[WTBDL_WORK_DESCRIBE]

    # 打印分割线
    print(DEVIDE_LINE)

    # 显示带索引的干员列表
    for idx, row in operator_df.iterrows():
        print(f"{idx}. QQ号: {row[WORKER_LIST_WORKER_NUMBER]}, 昵称: {row[ROW_NAME_WORKER_NAME]}, 工作总数: {row[WORKER_LIST_WORK_COUNT]}")

    while True:
        worker_idx = input("\n请输入干员编号(输入q退出): ")
        if worker_idx.lower() == 'q':
            print("用户取消手动导入")
            return operator_df,workflow_df,work_to_be_done_list,False
        
        try:
            worker_idx = int(worker_idx)
            if worker_idx < 0 or worker_idx >= len(operator_df):
                print(f"错误：编号必须在0-{len(operator_df)-1}范围内")
                continue
        except ValueError:
            print("错误：请输入有效的数字编号")
            continue
            
        # 获取选中的干员信息
        selected_worker = operator_df.iloc[worker_idx]
        qq = selected_worker[WORKER_LIST_WORKER_NUMBER]
        nickname = selected_worker[ROW_NAME_WORKER_NAME]
        
        # 生成新的工作流水号
        if not workflow_df.empty:
            new_id = workflow_df[WORK_ID].max() + 1
        else:
            new_id = 0
        
        # 创建工作记录
        print(f"您选中的干员是：{nickname}")
        work_date = datetime.now().strftime('%Y-%m-%d') + ' (手动导入)'
        
        new_record = {
            WORKER_LIST_WORKER_NUMBER: qq,
            ROW_NAME_WORKER_NAME: nickname,
            WORK_ID: new_id,
            WORK_DESCRIBE: description,
            WORK_ASSIGN_TIME: work_date
        }
        # 移除待完成工作表中的工作记录
        work_to_be_done_list = work_to_be_done_list[work_to_be_done_list[WTBDL_WORK_ID] != work_about_to_be_done_ID].copy()

        # 重新编号剩余工作的WTBDL_WORK_ID
        work_to_be_done_list.loc[:, WTBDL_WORK_ID] = range(len(work_to_be_done_list))

        # 更新数据
        workflow_df = workflow_df._append(new_record, ignore_index=True)
        operator_df.loc[operator_df[WORKER_LIST_WORKER_NUMBER] == qq, WORKER_LIST_WORK_COUNT] += 1

        # 保存文件
        save_tables(operator_df,workflow_df)
        save_to_be_done_list(work_to_be_done_list)
        
        return operator_df,workflow_df,work_to_be_done_list,True

# 从待完成工作表中自动选择工作并抽取人员完成
def auto_assign_work_from_to_be_done(
        operator_df:pd.DataFrame,#干员信息表
        workflow_df:pd.DataFrame,#工作记录表
        work_to_be_done_list:pd.DataFrame#待完成工作表
        ):
    """
    auto_assign_work_from_to_be_done 的 Docstring
    
    :param operator_df: 说明
    :type operator_df: pd.DataFrame
    :param workflow_df: 说明
    :type workflow_df: pd.DataFrame
    :param work_to_be_done_list: 说明
    :type work_to_be_done_list: pd.DataFrame
    """
    # 检查待完成工作表是否为空
    if len(work_to_be_done_list)<1:
        print("待完成工作表为空，请您先向待完成工作表中填写工作再通过本选项进行分配")
        return operator_df,workflow_df,work_to_be_done_list,False
    
    # 显示待完成工作表
    view_work_to_be_done_list(work_to_be_done_list)
    print("以上是我们所有等待分配的工作")

    # 获取要分配的工作序号
    work_about_to_be_done_ID = ask_for_number(0,len(work_to_be_done_list)-1,"请输入您要分配的待完成工作序号")

    # 获取待分配的工作的相关信息
    selected_work = work_to_be_done_list[work_to_be_done_list[WTBDL_WORK_ID] == work_about_to_be_done_ID].iloc[0]
    
    work_type = int(selected_work['工作类型'])
    description = selected_work['工作描述']

    # 打印分割线
    print(DEVIDE_LINE)

    # 自动分配工作？
    selceted_worker_qq,selected_worker_name=assign_work(operator_df,work_type)

    # 打印信息和确认
    print(f"建议分配干员：{selected_worker_name}")
    print(f"您要给他分配的工作是：{description}")

    # 若用户同意安排此项工作
    if(ask_for_yes_or_no(f"请问是否安排 {selected_worker_name} 从事 {description}?(y/n)")):
        # 生成新流水号
        if not workflow_df.empty:
            new_id = workflow_df[WORK_ID].max() + 1
        else:
            new_id = 0
        
        # 获取工作时间
        work_date = datetime.now().strftime('%Y-%m-%d')
        
        # 编写新工作记录
        new_record = {
            WORKER_LIST_WORKER_NUMBER: selceted_worker_qq,
            ROW_NAME_WORKER_NAME: selected_worker_name,
            WORK_ID: new_id,
            WORK_DESCRIBE: description,
            WORK_ASSIGN_TIME: work_date
        }
        # 移除待完成工作表中的工作记录
        work_to_be_done_list = work_to_be_done_list[work_to_be_done_list[WTBDL_WORK_ID] != work_about_to_be_done_ID].copy()

        # 重新编号剩余工作的WTBDL_WORK_ID
        work_to_be_done_list.loc[:, WTBDL_WORK_ID] = range(len(work_to_be_done_list))

        # 更新数据
        workflow_df = workflow_df._append(new_record, ignore_index=True)
        operator_df.loc[operator_df[WORKER_LIST_WORKER_NUMBER] == selceted_worker_qq, WORKER_LIST_WORK_COUNT] += 1

        # 保存文件
        save_tables(operator_df,workflow_df)
        save_to_be_done_list(work_to_be_done_list)
        
        print("工作分配完成")
        return operator_df,workflow_df,work_to_be_done_list,True
    # 若用户不同意安排此项工作
    else:
        print("用户取消")
        return operator_df,workflow_df,work_to_be_done_list,False

###############################################
##############      表格预览功能    ########################
###############################################
# 预览干员名单
def view_operator_df(operator_df):
    for idx, row in operator_df.iterrows():
        print(f"{idx}. QQ号: {row[WORKER_LIST_WORKER_NUMBER]}, 昵称: {row[ROW_NAME_WORKER_NAME]}, 工作总数: {row[WORKER_LIST_WORK_COUNT]}")

# 预览工作记录
def view_workflow_df(workflow_df):
    print("\n当前所有工作记录:")
    print(workflow_df[[WORK_ID, ROW_NAME_WORKER_NAME, WORK_DESCRIBE, WORK_ASSIGN_TIME]].to_string(index=False))

# 预览待完成工作表
def view_work_to_be_done_list(work_to_be_done_list):
    print("\n当前待完成工作")
    print(work_to_be_done_list[[WTBDL_WORK_ID, WTBDL_WORK_DESCRIBE, WTBDL_ASSIGN_TIME]].to_string(index=False))

def help_message():
    print("这里是帮助文档，抱歉我还没写完")

CHOICE_CSV_INIT='0'# 重新初始化
CHOICE_NEW_WORK='1'# 分配新工作
CHOICE_DELETE_WORK_RECORD='2'# 删除工作记录
CHOICE_MANUAL_IMPORT='3'# 手动导入工作记录
CHOICE_VIEW_WORK_FLOW='4'# 预览工作记录表
CHOICE_VIEW_OPERATOR='5'# 预览干员信息表
CHOICE_ADD_WORK_TO_BE_DONE='6'# 注册待完成工作
CHOICE_VIEW_WORK_TO_BE_DONE_LIST='7'# 预览待完成工作
CHOICE_NEW_WORK_FROM_TO_BE_DONE_LIST='8'# 从待完成工作表中选择一项工作分配
CHOICE_HELP = '9'
CHOICE_QUIT='q'
CHOICE_LIST=['0. 重新初始化',"1. 分配新工作","2. 删除工作记录","3. 手动导入工作记录","4. 预览工作记录表",
             "5. 预览干员信息表","6. 注册待完成工作","7. 预览待完成工作表","8. 从待完成工作表中选择一项工作分配","9. 使用帮助",
             "q. 退出"]

def main():
    # 程序初始化
    csv_init()
    operator_df, workflow_df , work_to_be_done_list = load_tables()

    while True:
        print("\n===== 工作分配系统 =====")
        for i in range(len(CHOICE_LIST)):
            print(CHOICE_LIST[i])

        choice = input("请选择操作: ").lower()
        
        if choice == CHOICE_QUIT:
            break
        # 初始化
        if choice == CHOICE_CSV_INIT:
            csv_init()
        # 分配新工作
        elif choice == CHOICE_NEW_WORK:
            operator_df,workflow_df,work_to_be_done_list,flag=auto_assign_work_from_to_be_done(operator_df,workflow_df,work_to_be_done_list)
            """
            print("\n请输入当前工作类型:")
            for i, work_type in enumerate(work_type_list, 1):
                print(f"{i}. {work_type}")
                
            work_type = input("\n输入q返回: ")
            if work_type.lower() == 'q':
                continue
                
            if not work_type.isdigit() or int(work_type) < 1 or int(work_type) > 9:
                print("错误：工作类型必须是1-9的数字")
                continue
                
            work_type = int(work_type)
            qq, nickname = assign_work(operator_df, work_type)
            
            if qq is None:
                continue
                
            print(f"\n建议分配干员: QQ号 {qq}, 昵称 {nickname}")
            
            while True:
                confirm = input("是否由该干员承担工作？(y/n): ").lower()
                if confirm in ['y', 'n']:
                    break
                print("请输入y或n")
            
            if confirm == 'n':
                print("重新分配干员...")
                continue
                
            if not workflow_df.empty:
                new_id = workflow_df[WORK_ID].max() + 1
            else:
                new_id = 0
                
            description = input("请输入工作内容描述: ")
            work_date = datetime.now().strftime('%Y-%m-%d')
            
            new_record = {
                'QQ号': qq,
                '干员昵称': nickname,
                '工作流水号': new_id,
                '工作描述': description,
                '工作日期': work_date
            }
            workflow_df = workflow_df._append(new_record, ignore_index=True)
            operator_df.loc[operator_df[WORKER_LIST_WORKER_NUMBER] == qq, WORKER_LIST_WORK_COUNT] += 1

            save_tables(operator_df, workflow_df)
            print("工作分配已记录！")
        """
        # 删除工作记录
        elif choice == CHOICE_DELETE_WORK_RECORD:
            operator_df, workflow_df, deleted = delete_work_record(operator_df, workflow_df)
            if deleted:
                save_tables(operator_df, workflow_df)
                print("工作记录已删除并更新干员信息！")
        # 手动导入工作记录
        elif choice == CHOICE_MANUAL_IMPORT:
            print("\n手动导入工作记录")
            manual_flag=ask_for_number(0,1,"0：从待完成工作表选择，\n1：手动输入工作描述\n2：取消")
            if manual_flag==0:
                print("从待完成工作表选择")
                operator_df,workflow_df,work_to_be_done_list,_=manual_assign_work_from_to_be_done(operator_df,workflow_df,work_to_be_done_list)
            elif manual_flag==1:
                print("手动输入工作描述")
                operator_df,workflow_df = manual_import_work(operator_df,workflow_df)
            elif manual_flag==2:
                print("用户取消")
        # 预览工作记录表
        elif choice == CHOICE_VIEW_WORK_FLOW:
            view_workflow_df(workflow_df)
        # 预览干员信息表
        elif choice == CHOICE_VIEW_OPERATOR:
            view_operator_df(operator_df)
        # 向待完成工作表中增加一项工作
        elif choice == CHOICE_ADD_WORK_TO_BE_DONE:
            work_to_be_done_list = add_a_new_work(work_to_be_done_list)
        # 预览待完成工作表
        elif choice == CHOICE_VIEW_WORK_TO_BE_DONE_LIST:
            view_work_to_be_done_list(work_to_be_done_list)
        # 使用帮助
        elif choice == CHOICE_HELP:
            help_message()
        else:
            print("错误：无效的选择，请输入数字0~6或q")
            
if __name__ == "__main__":
    main()