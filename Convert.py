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
battle_log_all = {}
for file in dir_files:
    if file[:6] == 'battle':
        battle_log_single = json.loads(open('json/' + file, 'r+').read())
        battle_log_all = dict(battle_log_all, **battle_log_single)

lap_max = 0
for battle_log in battle_log_all.keys():
    if battle_log_all[battle_log]['lap'] > lap_max:
        lap_max = battle_log_all[battle_log]['lap']
for lap in range(1, lap_max+1):
    for order in range(1, 6):
        time_damage = {}
        for battle_log in battle_log_all.keys():
            if battle_log_all[battle_log]['lap'] == lap and battle_log_all[battle_log]['order'] == order:
                time_damage[battle_log_all[battle_log]['time']]= battle_log_all[battle_log]

        damage_order = sorted(time_damage.items(), key=lambda x:x[0], reverse=True)
        if damage_order:
            for i, damage_tuple in enumerate(damage_order):
                if_extra = 0
                if damage_tuple[1]['lap'] > 44 and damage_tuple[1]['damage'] < 10000000:
                    if_extra = 1
                battle_date = time.strftime("%m%d", time.localtime(damage_tuple[0] - 18000))
                user_stat[battle_date][str(damage_tuple[1]['viewer_id'])]['battle'][str(damage_tuple[1]['lap'])+'-'+str(damage_tuple[1]['order'])+('尾' if i == 0 else '')+('补' if if_extra == 1 else '')] = damage_tuple[1]['damage']

for date in date_list:
    write_str_all = ''
    for user in user_stat[date].keys():
        write_str = ''
        finish_num = 0
        if user_stat[date][user]['battle']:
            battle_user = sorted(user_stat[date][user]['battle'].items(), key=lambda x: x[1], reverse=True)
            for battle in battle_user:
                write_str += '(' + battle[0] + ')' + str(battle[1]) + ','
                if '补' in battle[0] or '尾' in battle[0]:
                    finish_num += 0.5
                else:
                    finish_num += 1
        if finish_num > 3:
            finish_num = 3
        write_str_all += user_stat[date][user]['name'] + ',' + str(finish_num) + ',' + write_str + '\n'
    with open('csv/' + date + '.csv', 'w') as f:
        f.write(write_str_all)
