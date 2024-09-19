import pandas as pd
import re
import time

def process_text(text):
    lst = text.split("\n\n")
    # 对列表中的每个元素进行判断并处理
    result = [(s[0:-2], s[-2:]) if s[-2:] == 'No' else (s[0:-3], s[-3:]) for s in lst]
    return result

start_time = time.time()

df = pd.read_json('./test.json')

new_rows = []

for idx, row in df.iterrows():
    input_text = row['input']
    original_id = row['id']
    options = row['options']
    gold_index = row['gold_index']
    class_id = row['class_id']
    Q_A = process_text(input_text)
    for (Question, answer) in Q_A:
        new_row = {
            'Question': Question,
            'Answer': answer,
            'Original_id': original_id,
            'options': options,
            'gold_index': gold_index,
            'class_id': class_id
        }
        new_rows.append(new_row)

# 创建新的DataFrame
new_df = pd.DataFrame(new_rows)

df_filtered = new_df[new_df['Answer'].isin(['Yes', 'No'])] # 过滤掉Answer列中不是'Yes'或'No'的行
df_reset = df_filtered.reset_index(drop=True)
df_reset = df_reset.reset_index()
df_res = df_reset.rename(columns={'index': 'id'})
end_time = time.time()
uesed_time = end_time - start_time

print(f"程序运行时间：{uesed_time}秒")

df_res.to_json('output.json', orient='records',lines=True)
