import pandas as pd
import random
from datetime import datetime
import os

# 三张表格的路径
WORKER_LIST_FILE_NAME = '1号表干员信息表.csv'
WORK_FLOW_FILE_NAME = '2号表工作流记录表.csv'
PATH_WORK_TO_BE_DONE_LIST = '3号待完成工作表.csv'

# 存放你们社团的工作分工
work_type_list = ['线下工作', '设计工作', '行政工作', '采购工作', '策划工作', 
                 '内建内训', '外联工作', '玉衡特别行动组', '星弦游戏工作室']

# 干员信息表和待完成工作表用到的常量
ROW_NAME_WORK_COUNT = '已经从事过的工作数量'
ROW_NAME_WORKER_NUMBER = 'QQ号'
ROW_NAME_WORKER_NAME = '干员昵称'
WORK_ID = '工作流水号'
WORK_DESCRIBE = '工作描述'
WORK_ASSIGN_TIME='工作日期'

# 待完成工作表常量
WTBDL_WORK_ID = '待完成工作序号'
WTBDL_WORK_DESCRIBE = '工作描述'
WTBDL_ASSIGN_TIME = '工作注册时间'

# 表头名称
WORK_TO_BE_DONE_LIST_COLUMN_NAME=[WTBDL_WORK_ID,WTBDL_WORK_DESCRIBE,WTBDL_ASSIGN_TIME]
WORK_FLOW_COLUMN_NAME=[ROW_NAME_WORKER_NUMBER,ROW_NAME_WORKER_NAME,WORK_ID,WORK_DESCRIBE,WORK_ASSIGN_TIME]

############################
#工具函数
##############################
def load_tables():
    """从文件加载表格
    Returns:
        operator_df:干员名单
        workflow_df:工作记录
        path_work_to_be_done_list:待完成工作表
    """
    try:
        operator_df = pd.read_csv(WORKER_LIST_FILE_NAME)
        workflow_df = pd.read_csv(WORK_FLOW_FILE_NAME)
        work_to_be_done_list = pd.read_csv(PATH_WORK_TO_BE_DONE_LIST)
        return operator_df, workflow_df ,work_to_be_done_list
    except FileNotFoundError:
        print("错误：未找到数据文件，请确保1号表和2号表存在")
        exit()

def save_tables(operator_df, workflow_df):
    """保存员工工作表和工作记录表
    """
    operator_df.to_csv(WORKER_LIST_FILE_NAME, index=False)
    workflow_df.to_csv(WORK_FLOW_FILE_NAME, index=False)

def save_to_be_done_list(work_to_be_done_list):
    """保存待完成工作标
    """
    work_to_be_done_list.to_csv(PATH_WORK_TO_BE_DONE_LIST, index=False)

def assign_work(operator_df, work_type):
    """自动随机分配工作，获取被抽中人的相关信息
    """
    preferred_operators = operator_df[operator_df[work_type_list[work_type-1]] == 1]
    
    if preferred_operators.empty:
        print(f"没有干员倾向于从事工作类型{work_type_list[work_type-1]}")
        return None, None
    
    min_work_count = preferred_operators[ROW_NAME_WORK_COUNT].min()
    candidates = preferred_operators[preferred_operators[ROW_NAME_WORK_COUNT] == min_work_count]
    
    selected_operator = candidates.sample(1).iloc[0]
    return selected_operator[ROW_NAME_WORKER_NUMBER], selected_operator[ROW_NAME_WORKER_NAME]

# 检查表格是否存在
def weather_tables_exsit():
    file_path=WORKER_LIST_FILE_NAME
    if os.path.exists(file_path):
        print(f"\n文件 '{file_path}' 已经存在")
    else:
        print(f"\n文件 '{file_path}' 不存在")

    file_path=WORK_FLOW_FILE_NAME
    if os.path.exists(file_path):
        print(f"\n文件 '{file_path}' 已经存在")
    else:
        print(f"\n文件 '{file_path}' 不存在")

    file_path=PATH_WORK_TO_BE_DONE_LIST
    if os.path.exists(file_path):
        print(f"\n文件 '{file_path}' 已经存在")
    else:
        print(f"\n文件 '{file_path}' 不存在")

# 根据表头名称检查表格是否符合格式要求，相符返回0，否则返回1
def tables_column_name_check(table_to_be_check_file_path:str,column_name:str)->int:
    # 检查表格是否存在
    try:
        table_to_be_check=pd.read_csv(table_to_be_check_file_path)
    except FileNotFoundError:
        print("错误：运行tables_column_name_check函数时未找到文件")
        return 0
    
    headers = table_to_be_check.columns.tolist()
    if(len(headers)!=len(column_name)):
        print(f"\n位于{table_to_be_check_file_path}的表格表头的长度与程序设定的表头长度不一致，程序设定的表格长度为{len}")
        print(f"\n表格头应该为{column_name}")
    # 遍历表头名称列表，取出csv表格的表头逐个对比
    for index, name in enumerate(column_name):
        if(name!=headers[index]):
            print(f"\n位于{table_to_be_check_file_path}的表格头内容与程序设定的不一致")
            print(f"\n文件中的表格头为{name}")
            print(f"\n程序期望的表格头为{headers[index]}")
        return 0
    return 1

##########################################
#手动操作
##########################################
# 手动删除工作记录
def delete_work_record(operator_df, workflow_df):
    print("\n当前所有工作记录:")
    print(workflow_df[[WORK_ID, ROW_NAME_WORKER_NAME, '工作内容描述', '工作日期']])
    
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
    
    qq = record[ROW_NAME_WORKER_NUMBER]
    operator_df.loc[operator_df[ROW_NAME_WORKER_NUMBER] == qq, ROW_NAME_WORK_COUNT] -= 1
    workflow_df = workflow_df[workflow_df[WORK_ID] != record_id]
    
    return operator_df, workflow_df, True

# 手动导入工作记录
def manual_import_work(operator_df, workflow_df):
    print("\n当前所有干员列表:")
    # 显示带索引的干员列表
    for idx, row in operator_df.iterrows():
        print(f"{idx}. QQ号: {row[ROW_NAME_WORKER_NUMBER]}, 昵称: {row[ROW_NAME_WORKER_NAME]}, 工作总数: {row[ROW_NAME_WORK_COUNT]}")
    
    while True:
        worker_idx = input("\n请输入干员编号(输入q退出): ")
        if worker_idx.lower() == 'q':
            return operator_df, workflow_df, False
        
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
        qq = selected_worker[ROW_NAME_WORKER_NUMBER]
        nickname = selected_worker[ROW_NAME_WORKER_NAME]
        
        # 生成新的工作流水号
        if not workflow_df.empty:
            new_id = workflow_df[WORK_ID].max() + 1
        else:
            new_id = 1
        
        # 创建工作记录
        print(f"您选中的干员是：{nickname}")
        description = input("请输入工作内容描述: ")
        work_date = datetime.now().strftime('%Y-%m-%d') + ' (手动导入)'
        
        new_record = {
            'QQ号': qq,
            '干员昵称': nickname,
            '工作流水号': new_id,
            '工作内容描述': description,
            '工作日期': work_date
        }
        
        # 更新数据
        workflow_df = workflow_df._append(new_record, ignore_index=True)
        operator_df.loc[operator_df[ROW_NAME_WORKER_NUMBER] == qq, ROW_NAME_WORK_COUNT] += 1
        
        return operator_df, workflow_df, True

# 手动向待完成工作表中填写一个新工作
def add_a_new_work(work_to_be_done_list):
    print("\n该功能尚未完善")

# 表格初始化
def csv_init():
    csv1=
    csv2=
    csv3=

########################################
#表格预览功能
######################################
# 预览干员名单
def view_operator_df(operator_df):
    for idx, row in operator_df.iterrows():
        print(f"{idx}. QQ号: {row[ROW_NAME_WORKER_NUMBER]}, 昵称: {row[ROW_NAME_WORKER_NAME]}, 工作总数: {row[ROW_NAME_WORK_COUNT]}")

# 预览工作记录
def view_workflow_df(workflow_df):
    print("\n当前所有工作记录:")
    print(workflow_df[[WORK_ID, ROW_NAME_WORKER_NAME, WORK_DESCRIBE, WORK_ASSIGN_TIME]])

# 预览待完成工作表
def view_work_to_be_done_list(work_to_be_done_list):
    print("\n当前待完成工作")
    print(work_to_be_done_list[[WTBDL_WORK_ID, WTBDL_WORK_DESCRIBE, WTBDL_ASSIGN_TIME]])
    return

CHOICE_NEW_WORK='1'
CHOICE_DELETE_WORK_RECORD='2'
CHOICE_MANUAL_IMPORT='3'
CHOICE_VIEW_WORK_FLOW='4'
CHOICE_VIEW_OPERATOR='5'
CHOICE_QUIT='q'
CHOICE_ADD_WORK_TO_BE_DONE='6'
def main():
    operator_df, workflow_df , work_to_be_done_list= load_tables()
    
    while True:
        print("\n===== 工作分配系统 =====")
        print(CHOICE_NEW_WORK+". 分配新工作")
        print(CHOICE_DELETE_WORK_RECORD+". 删除工作记录")
        print(CHOICE_MANUAL_IMPORT+". 手动导入工作记录")
        print(CHOICE_VIEW_WORK_FLOW+". 预览工作记录")
        print(CHOICE_VIEW_OPERATOR+". 预览干员信息表")
        print(CHOICE_QUIT+". 退出")
        
        choice = input("请选择操作: ").lower()
        
        if choice == CHOICE_QUIT:
            break
        # 分配新工作
        if choice == CHOICE_NEW_WORK:
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
                new_id = 1
                
            description = input("请输入工作内容描述: ")
            work_date = datetime.now().strftime('%Y-%m-%d')
            
            new_record = {
                'QQ号': qq,
                '干员昵称': nickname,
                '工作流水号': new_id,
                '工作内容描述': description,
                '工作日期': work_date
            }
            workflow_df = workflow_df._append(new_record, ignore_index=True)
            operator_df.loc[operator_df[ROW_NAME_WORKER_NUMBER] == qq, ROW_NAME_WORK_COUNT] += 1

            save_tables(operator_df, workflow_df)
            print("工作分配已记录！")
        # 删除工作记录
        elif choice == CHOICE_DELETE_WORK_RECORD:
            operator_df, workflow_df, deleted = delete_work_record(operator_df, workflow_df)
            if deleted:
                save_tables(operator_df, workflow_df)
                print("工作记录已删除并更新干员信息！")
        # 手动导入工作记录
        elif choice == CHOICE_MANUAL_IMPORT:
            operator_df, workflow_df, manual_import = manual_import_work(operator_df, workflow_df)
            if manual_import:
                save_tables(operator_df, workflow_df)
                print("成功手动导入工作记录")
            else:
                print("用户取消手动导入")
        # 预览工作记录表
        elif choice == CHOICE_VIEW_WORK_FLOW:
            view_workflow_df(workflow_df)
        # 预览干员信息表
        elif choice == CHOICE_VIEW_OPERATOR:
            view_operator_df(operator_df)
        # 向待完成工作表中增加一项工作
        elif choice == CHOICE_ADD_WORK_TO_BE_DONE:
            work_to_be_done_list=add_a_new_work()
        else:
            print("错误：无效的选择，请输入1、2、3、4、5、6或q")
            
if __name__ == "__main__":
    main()