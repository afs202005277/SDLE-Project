from copy import deepcopy

last_sync_list = {
    'name': 'list_name',
    'items': [
        {
            'name': 'banana',
            'quantity': 23
        },
        {
            'name': 'apple',
            'quantity': 1
        }
    ]
}

cl1 = {
    'changelog': [
        {
            'operation': 'add',
            'item': 'banana',
            'quantity': 2
        },
        {
            'operation': 'remove',
            'item': 'apple',
            'quantity': 1
        }
    ]
}

cl2 = {
    'changelog': [
        {
            'operation': 'add',
            'item': 'milk',
            'quantity': 3
        },
        {
            'operation': 'remove',
            'item': 'banana',
            'quantity': 15
        }
    ]
}

class CRDT:
    def __init__(self, state):
        self.state = state
        self.changelogs = []
    
    def changelog(self, log):
        self.changelogs.append(log)

        for entry in log['changelog']:
            operation = entry['operation']
            item = entry['item']
            existingItem = [_item for _item in self.state['items'] if _item['name'] == item]

            if operation == 'add':
                if existingItem == []:
                    self.state['items'].append({'name': item, 'quantity': entry['quantity']})
                else:
                    existingItem[0]['quantity'] += entry['quantity']

            elif (operation == 'remove') and (len(existingItem) > 0):
                if entry['quantity'] >= existingItem[0]['quantity']:
                    self.state['items'] = list(filter(lambda x : x != existingItem[0], self.state['items']))
                else:
                    existingItem[0]['quantity'] -= entry['quantity']

    def merge(self, other):
        if self.state == other.state: return

        for log in other.changelogs:
            self.changelog(log)

        for log in self.changelogs:
            other.changelog(log)

    
if __name__ == '__main__':
    print(f'START LIST (LAST SYNC. FROM CLOUD)\n{last_sync_list}\n')

    crdt1 = CRDT(deepcopy(last_sync_list))
    crdt1.changelog(cl1)
    print(f'RESULTING CRDT FROM CHANGELOG 1\n{crdt1.state}\n')

    crdt2 = CRDT(deepcopy(last_sync_list))
    crdt2.changelog(cl2)
    print(f'RESULTING CRDT FROM CHANGELOG 2\n{crdt2.state}\n')

    crdt1.merge(crdt2)
    print(f'RESULTING CRDT FROM MERGE 2 INTO 1\n{crdt1.state}\n')
    print(f'RESULTING CRDT FROM MERGE 1 INTO 2\n{crdt1.state}\n')