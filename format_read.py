import pandas as pd
import random
from datetime import datetime

work_type_list = ['线下工作', '设计工作', '行政工作', '采购工作', '策划工作', 
                 '内建内训', '外联工作', '玉衡特别行动组', '星弦游戏工作室']

def load_tables():
    try:
        operator_df = pd.read_csv('1号表干员信息表.csv')
        workflow_df = pd.read_csv('2号表工作流记录表.csv')
        return operator_df, workflow_df
    except FileNotFoundError:
        print("错误：未找到数据文件，请确保1号表和2号表存在")
        exit()

def save_tables(operator_df, workflow_df):
    operator_df.to_csv('1号表干员信息表.csv', index=False)
    workflow_df.to_csv('2号表工作流记录表.csv', index=False)

def assign_work(operator_df, workflow_df, work_type):
    preferred_operators = operator_df[operator_df[work_type_list[work_type-1]] == 1]
    
    if preferred_operators.empty:
        print(f"没有干员倾向于从事工作类型{work_type_list[work_type-1]}")
        return None, None
    
    min_work_count = preferred_operators['已经从事过的工作数量'].min()
    candidates = preferred_operators[preferred_operators['已经从事过的工作数量'] == min_work_count]
    
    selected_operator = candidates.sample(1).iloc[0]
    return selected_operator['QQ号'], selected_operator['干员昵称']

def delete_work_record(operator_df, workflow_df):
    print("\n当前所有工作记录:")
    print(workflow_df[['工作流水号', '干员昵称', '工作内容描述', '工作日期']])
    
    while True:
        record_id = input("\n请输入要删除的工作流水号(输入q返回主菜单): ")
        if record_id.lower() == 'q':
            return operator_df, workflow_df, False
        
        if not record_id.isdigit():
            print("错误：请输入数字流水号")
            continue
            
        record_id = int(record_id)
        if record_id not in workflow_df['工作流水号'].values:
            print(f"错误：流水号{record_id}不存在")
            continue
            
        break
    
    # 获取要删除的记录
    record = workflow_df[workflow_df['工作流水号'] == record_id].iloc[0]
    
    # 确认删除
    print(f"\n将要删除以下记录:")
    print(record)
    confirm = input("确认删除吗？(y/n): ").lower()
    if confirm != 'y':
        return operator_df, workflow_df, False
    
    # 更新干员信息表
    qq = record['干员qq号']
    operator_df.loc[operator_df['QQ号'] == qq, '已经从事过的工作数量'] -= 1
    
    # 删除工作记录
    workflow_df = workflow_df[workflow_df['工作流水号'] != record_id]
    
    return operator_df, workflow_df, True

def main():
    operator_df, workflow_df = load_tables()
    
    while True:
        print("\n===== 工作分配系统 =====")
        print("1. 分配新工作")
        print("2. 删除工作记录")
        print("q. 退出")
        
        choice = input("请选择操作: ").lower()
        
        if choice == 'q':
            break
            
        if choice == '1':
            # 分配新工作逻辑
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
            qq, nickname = assign_work(operator_df, workflow_df, work_type)
            
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
                new_id = workflow_df['工作流水号'].max() + 1
            else:
                new_id = 1
                
            description = input("请输入工作内容描述: ")
            work_date = datetime.now().strftime('%Y-%m-%d')
            
            new_record = {
                '干员qq号': qq,
                '干员昵称': nickname,
                '工作流水号': new_id,
                '工作内容描述': description,
                '工作日期': work_date
            }
            workflow_df = workflow_df._append(new_record, ignore_index=True)
            operator_df.loc[operator_df['QQ号'] == qq, '已经从事过的工作数量'] += 1
            
            save_tables(operator_df, workflow_df)
            print("工作分配已记录！")
            
        elif choice == '2':
            # 删除工作记录逻辑
            operator_df, workflow_df, deleted = delete_work_record(operator_df, workflow_df)
            if deleted:
                save_tables(operator_df, workflow_df)
                print("工作记录已删除并更新干员信息！")
                
        else:
            print("错误：无效的选择，请输入1、2或q")
            
if __name__ == "__main__":
    main()