import os
import json
import time


user_stat = {}
battle_all = []
date_list = ['0423', '0424', '0425', '0426', '0427']
for date in date_list:
    user_stat[date] = {}
dir_files = os.listdir('json')
for file in dir_files:
    if file[:7] == 'members':
        user_name_dict = json.loads(open('json/' + file, 'r+').read())
        for date in date_list:
            for user in user_name_dict.keys():
                user_stat[date][user] = {
                    'name': user_name_dict[user]['user_name'],
                    'battle': {}
                }
for file in dir_files:
    if file[:6] == 'battle':
        user_battle_log = json.loads(open('json/' + file, 'r+').read())
        for user in user_battle_log.keys():
            user_log = user_battle_log[user]['battle_log']
            if user_log:
                for battle in user_log.keys():
                    if battle not in battle_all:
                        battle_all.append(battle)
                        battle_date = time.strftime("%m%d", time.localtime(user_log[battle]['time']-18000))
                        user_stat[battle_date][user]['battle'][str(user_log[battle]['lap'])+'-'+str(user_log[battle]['order'])] = user_log[battle]['damage']


for date in date_list:
    write_str = ''
    for user in user_stat[date].keys():
        write_str += user_stat[date][user]['name'] + ','
        if user_stat[date][user]['battle']:
            battle_user = sorted(user_stat[date][user]['battle'].items(), key=lambda x: x[1], reverse=True)
            for battle in battle_user:
                write_str += '(' + battle[0] + ')' + str(battle[1]) + ','
        write_str += '\n'
    with open('csv/' + date + '.csv', 'w') as f:
        f.write(write_str)
