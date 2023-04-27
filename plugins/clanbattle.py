import os
import json
from PCRoxy import PCRoxyMode
from PCRoxyFlowChain import HookCtx
from PCRoxyPlugin import PCRoxyPlugin

plugin = PCRoxyPlugin(name='BattleRecord', mode_list=[PCRoxyMode.OBSERVER])

mode = plugin.config['mode']

page = 0


@plugin.on_response(path='/clan/info')
async def DumpMembers(context: HookCtx):
    clan_members = {}
    clan_name = context.payload['data']['clan']['detail']['clan_name']
    for member in context.payload['data']['clan']['members']:
        clan_members[member['viewer_id']] = {
            'user_name': member['name'],
            'clan_point': member['clan_point']
        }
    json.dump(clan_members, open(f'./json/members_{clan_name}.json', 'w'))


@plugin.on_response(path='/clan_battle/battle_log_list')
async def DumpBattleLog(context: HookCtx):
    clan_name = ''
    dir_files = os.listdir('json')
    for file in dir_files:
        if file[:7] == 'members':
            clan_name = file[7:-5]
    battle_log_all = {}
    for battle in context.payload['data']['battle_list']:
        if battle['battle_type'] == 1:
            battle_log_all[battle['battle_log_id']] = {
                'viewer_id': battle['target_viewer_id'],
                'lap': battle['lap_num'],
                'order': battle['order_num'],
                'damage': battle['total_damage'],
                'time': battle['battle_end_time']
            }
    global page
    page += 1
    with open('json/battle' + clan_name + str(page) + '.json', 'w') as f:
        json.dump(battle_log_all, f, indent=4)
