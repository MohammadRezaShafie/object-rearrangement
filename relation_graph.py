import networkx as nx

def create_relation_graph():
    actions = [
    ('Apple', 'Apple_sliced', ['slice',['Knife', 'ButterKnife']]),
    
    ('Tomato', 'Tomato_sliced', ['slice',['Knife', 'ButterKnife']]),
    
    ('Lettuce', 'Lettuce_sliced', ['slice',['Knife', 'ButterKnife']]),    
        
    ('Book', 'Book_opened', ['open', ['Hand']]),
    ('Book_opened', 'Book', ['close', ['Hand']]),
    
    ('Cabinet', 'Cabinet_opened', ['open', ['Hand']]),
    ('Cabinet_opened', 'Cabinet', ['close', ['Hand']]),
    
    ('Drawer', 'Drawer_opened', ['open', ['Hand']]),
    ('Drawer_opened', 'Drawer', ['close', ['Hand']]),
    
    ('Fridge', 'Fridge_opened', ['open', ['Hand']]),
    ('Fridge_opened', 'Fridge', ['close', ['Hand']]),

    ('Microwave', 'Microwave_opened', ['open', ['Hand']]),
    ('Microwave_opened', 'Microwave', ['close', ['Hand']]),
      
    ('Potato', 'Potato_sliced', ['slice',['Knife', 'ButterKnife']]),
    ('Potato_sliced', 'Potato_sliced_cooked', ['cook', ['Stove']]),
    ('Potato', 'Potato_cooked', ['cook', ['Stove']]),
    ('Potato_cooked', 'Potato_sliced_cooked', ['slice',['Knife', 'ButterKnife']]),
    
    ('Bread', 'Bread_sliced', ['slice',['Knife', 'ButterKnife']]),
    ('Bread_sliced', 'Bread_sliced_cooked', ['cook', ['Toaster']]),

    ('Egg', 'Egg_sliced', ['slice',['Hand', 'Knife', 'ButterKnife']]),
    ('Egg_sliced', 'Egg_sliced_cooked', ['cook', ['Stove']]),
    
    
    ('Mug', 'Mug_filled', ['fill', ['CoffeMachine', 'Faucet']]),
    ('Mug_filled', 'Mug', ['empty', ['Sink']]),   
 
    ('Pot', 'Pot_filled', ['fill',  ['Faucet']]),
    ('Pot_filled', 'Pot', ['empty', ['Sink']]),     

    ('WineBottle', 'WineBottle_filled', ['fill',  ['Faucet']]),
    ('WineBottle_filled', 'WineBottle', ['empty', ['Sink']]),
            
    ('Bottle', 'Bottle_filled',['fill',  ['Faucet']]),
    ('Bottle_filled', 'Bottle', ['empty', ['Sink']]),
    
    ('Cup', 'Cup_filled', ['fill', ['CoffeMachine', 'Faucet']]),
    ('Cup_filled', 'Cup', ['empty', ['Sink']]),
    
    ('Bowl', 'Bowl_filled', ['fill', ['CoffeMachine', 'Faucet']]),
    ('Bowl_filled', 'Bowl', ['empty', ['Sink']]),
    ]
    
    G = nx.DiGraph()
    for action in actions:
        G.add_edge(action[0], action[1], action=action[2])
    
    return G