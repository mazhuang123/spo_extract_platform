import json
import requests
import pandas as pd
from tqdm import tqdm
from pyltp import SentenceSplitter
import config
# 小说的名称

# txt文件读取
with open(config.book_path, 'r', encoding='UTF-8') as f:
    content = f.read()

sents = [_.strip().replace(" ", "") for _ in list(SentenceSplitter.split(content)) if _.strip()]


# 逐句抽取并保留抽取结果至列表中
texts = []
subject_list, times_list, spo_dic_list = [], [], []
spo_result_list = []
only_spo_list = [] #存的是所有三元关系组

def isExistInSpoList(sub):
    for temp_spo in spo_result_list:
        if temp_spo['subject'] == sub or temp_spo['subject'] in sub or sub in temp_spo['subject']:
            temp_spo["times"]+=1
            return True,spo_result_list.index(temp_spo)
    return False,None

bar = tqdm(sents)
for ch, line in zip(bar, sents):
    req = requests.post("http://localhost:12308/spo_extract", data={"text": line})
    res = json.loads(req.content)

    if res:
        print("\n原文: %s" % line)
        for item in res:
            spo_dic = {}
            subj = item["object"]
            pred = item["predicate"]
            obj = item["subject"]

            spo_dic["S"] = subj
            spo_dic["P"] = pred
            spo_dic["O"] = obj
            if spo_dic["S"] == spo_dic["O"] or len(spo_dic["P"]) == 1:
                continue

            isExist, temp_spo_index= isExistInSpoList(subj)
            if isExist:
                spo_result_list[temp_spo_index]['spo'].append(spo_dic)
            else:
                new_sub_dic = {}
                new_sub_dic['subject'] = subj
                new_sub_dic['times'] = 1
                single_spo_list = []
                single_spo_list.append(spo_dic)
                new_sub_dic['spo'] = single_spo_list
                spo_result_list.append(new_sub_dic)

for single_spo in spo_result_list:
    subject_list.append(single_spo['subject'])
    times_list.append(single_spo['times'])
    spo_dic_list.append(single_spo['spo'])

filter_list = times_list
for temp_times in filter_list:
    if temp_times<=3:
        index  = filter_list.index(temp_times)
        subject_list.pop(index)
        times_list.pop(index)
        spo_dic_list.pop(index)

for temp_single_list in spo_dic_list:
    for temp_single_spo in temp_single_list:
        only_spo_list.append(temp_single_spo)

spo_subject_list = []
spo_pre_list = []
spo_obj_list = []
for sub_spo in only_spo_list:
    pre_subject = sub_spo['S']
    pre_object = sub_spo['O']
    pre_predicate = sub_spo['P']
    # for obj_spo in only_spo_list:
    #     next_subject = obj_spo['S']
    #     next_object = obj_spo['O']
    #     if pre_subject == next_object and pre_object == next_subject:
    #         # print("之前的: "+next_subject+"  "+next_object)
    #         next_subject = pre_object
    #         next_object = pre_subject
    #         # print("之后的: "+next_subject+"  "+next_object)


    spo_subject_list.append(pre_subject)
    spo_pre_list.append(pre_predicate)
    spo_obj_list.append(pre_object)

content = str(only_spo_list)

print(content)
filename = config.spo_file_name
with open(filename, 'w') as file_object:
    file_object.write(content)



# gpt_out_content = gpt3get.requestChatGpt()

# print(subject_list)
# print(times_list)
# print(spo_dic_list)
# 将抽取的三元组结果保存成EXCEL文件
# df = pd.DataFrame({"subject": spo_subject_list,
#                    "predicate": spo_pre_list,
#                    "object": spo_obj_list,
#                    })
#
# df.to_excel(config.excel_path, index=False)

