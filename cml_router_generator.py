import yaml
import math

def read_input_file(file_path):
    connections = []
    routers = set()  # Tüm router'ları ve switch'leri tutmak için bir küme
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 4:
                connections.append({
                    'source_router': parts[0],
                    'source_interface': parts[1],
                    'target_router': parts[2],
                    'target_interface': parts[3]
                })
                routers.add(parts[0])  # Kaynak router/switch'i ekle
                routers.add(parts[2])  # Hedef router/switch'i ekle
    return connections, sorted(routers)  # Router/switch'leri sıralı olarak döndür

def calculate_distance(x1, y1, x2, y2):
    # İki nokta arasındaki mesafeyi hesapla (Öklid mesafesi)
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def create_yaml_structure(connections, routers):
    # Merkez router (R1) için sabit koordinatlar
    center_x, center_y = 0, 0
    radius = 200  # Dairenin yarıçapı
    num_routers = len(routers)  # Toplam router/switch sayısı

    yaml_structure = {
        'annotations': [],
        'smart_annotations': [],
        'nodes': [],
        'links': [],
        'lab': {
            'description': '',
            'notes': '',
            'title': 'Lab at Fri 19:45 PM',
            'version': '0.3.0'
        }
    }

    # Router ve switch'leri sıralı bir şekilde oluştur
    router_to_id = {}  # Router/switch isimlerini ID'lere eşleştirmek için sözlük
    switch_counter = 1  # Switch'ler için sayaç (SW1, SW2, ...)
    router_positions = {}  # Router'ların koordinatlarını tutmak için sözlük

    # Önce router'ları (R veya r ile başlayanlar), ardından switch'leri (S veya s ile başlayanlar) sırala
    sorted_routers = sorted(routers, key=lambda x: (not x.lower().startswith('r'), x.lower()))

    for i, router in enumerate(sorted_routers):
        if router.lower() == 'r1':
            # R1'i merkeze yerleştir
            x, y = center_x, center_y
        elif router.lower().startswith('s') or router.startswith('S'):
            # Switch'ler için en yakın router'ın koordinatlarını bul
            closest_router = None
            min_distance = float('inf')
            closest_x, closest_y = 0, 0

            # Tüm router'lar arasında en yakın olanı bul
            for r, (rx, ry) in router_positions.items():
                distance = calculate_distance(rx, ry, closest_x, closest_y)
                if distance < min_distance:
                    min_distance = distance
                    closest_router = r
                    closest_x, closest_y = rx, ry

            # En yakın router'ın koordinatlarına yakın bir yere yerleştir
            x = closest_x + 50  # Örnek olarak 50 birim sağa kaydır
            y = closest_y + 50  # Örnek olarak 50 birim yukarı kaydır
        else:
            # Diğer router'ları daire üzerinde eşit açılarla yerleştir
            angle = 2 * math.pi * (i - 1) / (num_routers - 1)  # Açı hesaplama
            x = int(center_x + radius * math.cos(angle))  # X koordinatı (tam sayıya dönüştür)
            y = int(center_y + radius * math.sin(angle))  # Y koordinatı (tam sayıya dönüştür)

        router_id = f'n{i}'  # Router/switch ID'si (n0, n1, n2, ...)
        router_to_id[router] = router_id  # Router/switch ismini ID'ye eşle

        # Router ve switch'ler için node_definition ve label belirle
        if router.startswith('r'):
            node_definition = 'iol-xe'  # r ile başlayan router'lar için
            label = router.upper()  # Router etiketi (R1, R2, R3, ...)
            router_positions[router] = (x, y)  # Router'ın koordinatlarını kaydet
        elif router.startswith('R'):
            node_definition = 'iosv'  # R ile başlayan router'lar için
            label = router.upper()  # Router etiketi (R1, R2, R3, ...)
            router_positions[router] = (x, y)  # Router'ın koordinatlarını kaydet
        elif router.startswith('s'):
            node_definition = 'ioll2-xe'  # s ile başlayan switch'ler için
            label = f'SW{switch_counter}'  # Switch etiketi (SW1, SW2, ...)
            switch_counter += 1  # Switch sayacını artır
        elif router.startswith('S'):
            node_definition = 'iosvl2'  # S ile başlayan switch'ler için
            label = f'SW{switch_counter}'  # Switch etiketi (SW1, SW2, ...)
            switch_counter += 1  # Switch sayacını artır

        # Interface labellarını node_definition'a göre belirle
        if node_definition in ['iol-xe', 'ioll2-xe']:
            interface_labels = [
                {'id': 'i0', 'label': 'Loopback0', 'mac_address': None, 'type': 'loopback'},
                {'id': 'i1', 'label': 'Ethernet0/0', 'mac_address': None, 'slot': 0, 'type': 'physical'},
                {'id': 'i2', 'label': 'Ethernet0/1', 'mac_address': None, 'slot': 1, 'type': 'physical'},
                {'id': 'i3', 'label': 'Ethernet0/2', 'mac_address': None, 'slot': 2, 'type': 'physical'},
                {'id': 'i4', 'label': 'Ethernet0/3', 'mac_address': None, 'slot': 3, 'type': 'physical'}
            ]
        else:  # iosv veya iosvl2 için GigabitEthernet
            interface_labels = [
                {'id': 'i0', 'label': 'Loopback0', 'mac_address': None, 'type': 'loopback'},
                {'id': 'i1', 'label': 'GigabitEthernet0/0', 'mac_address': None, 'slot': 0, 'type': 'physical'},
                {'id': 'i2', 'label': 'GigabitEthernet0/1', 'mac_address': None, 'slot': 1, 'type': 'physical'},
                {'id': 'i3', 'label': 'GigabitEthernet0/2', 'mac_address': None, 'slot': 2, 'type': 'physical'},
                {'id': 'i4', 'label': 'GigabitEthernet0/3', 'mac_address': None, 'slot': 3, 'type': 'physical'}
            ]

        yaml_structure['nodes'].append({
            'boot_disk_size': None,
            'configuration': [],
            'cpu_limit': None,
            'cpus': None,
            'data_volume': None,
            'hide_links': False,
            'id': router_id,
            'image_definition': None,
            'label': label,
            'node_definition': node_definition,
            'parameters': {},
            'ram': None,
            'tags': [],
            'x': x,
            'y': y,
            'interfaces': interface_labels
        })

    # Arayüz isimlerini eşleştirme
    interface_to_id = {
        'Ethernet0/0': 'i1',
        'Ethernet0/1': 'i2',
        'Ethernet0/2': 'i3',
        'Ethernet0/3': 'i4',
        'Ethernet1/0': 'i1',
        'Ethernet1/1': 'i2',
        'Ethernet1/2': 'i3',
        'Ethernet1/3': 'i4',
        'GigabitEthernet0/0': 'i1',
        'GigabitEthernet0/1': 'i2',
        'GigabitEthernet0/2': 'i3',
        'GigabitEthernet0/3': 'i4',
        'GigabitEthernet1/0': 'i1',
        'GigabitEthernet1/1': 'i2',
        'GigabitEthernet1/2': 'i3',
        'GigabitEthernet1/3': 'i4',
        'e0/0': 'i1',
        'e0/1': 'i2',
        'e0/2': 'i3',
        'e0/3': 'i4',
        'e1/0': 'i1',
        'e1/1': 'i2',
        'e1/2': 'i3',
        'e1/3': 'i4',
        'g0/0': 'i1',
        'g0/1': 'i2',
        'g0/2': 'i3',
        'g0/3': 'i4',
        'g1/0': 'i1',
        'g1/1': 'i2',
        'g1/2': 'i3',
        'g1/3': 'i4'
    }

    # Bağlantıları oluştur
    used_interfaces = set()  # Kullanılan interface'leri takip etmek için küme
    for conn in connections:
        # Arayüz isimlerini dönüştür (e0/0 -> Ethernet0/0, g0/1 -> GigabitEthernet0/1, vb.)
        source_interface = conn['source_interface']
        target_interface = conn['target_interface']

        # Eğer interface ismi "e" ile başlıyorsa, "Ethernet" olarak dönüştür
        if source_interface.startswith('e'):
            source_interface = f"Ethernet{source_interface[1:]}"
        elif source_interface.startswith('g'):
            source_interface = f"GigabitEthernet{source_interface[1:]}"

        if target_interface.startswith('e'):
            target_interface = f"Ethernet{target_interface[1:]}"
        elif target_interface.startswith('g'):
            target_interface = f"GigabitEthernet{target_interface[1:]}"

        # Interface'lerin daha önce kullanılıp kullanılmadığını kontrol et
        source_key = (router_to_id[conn['source_router']], interface_to_id[source_interface])
        target_key = (router_to_id[conn['target_router']], interface_to_id[target_interface])

        if source_key in used_interfaces or target_key in used_interfaces:
            print(f"Warning: Interface already used in another link. Skipping connection: {conn}")
            continue  # Bu bağlantıyı atla

        # Interface'leri kullanılanlar listesine ekle
        used_interfaces.add(source_key)
        used_interfaces.add(target_key)

        link = {
            'id': f'l{len(yaml_structure["links"])}',
            'n1': router_to_id[conn['source_router']],
            'n2': router_to_id[conn['target_router']],
            'i1': interface_to_id[source_interface],
            'i2': interface_to_id[target_interface],
            'conditioning': {},
            'label': f'{conn["source_router"].upper()}-{source_interface}<->{conn["target_router"].upper()}-{target_interface}'
        }
        yaml_structure['links'].append(link)

    return yaml_structure

def write_yaml_file(yaml_structure, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(yaml_structure, file, sort_keys=False)

def main():
    input_file = 'input.txt'
    output_file = 'Router_Configuration.yaml'

    # Dosyayı oku ve bağlantıları ve router'ları al
    connections, routers = read_input_file(input_file)
    
    # YAML yapısını oluştur
    yaml_structure = create_yaml_structure(connections, routers)
    
    # YAML dosyasını yaz
    write_yaml_file(yaml_structure, output_file)
    
    # Başarı mesajı
    print("Successfully created Router_Configuration.yaml file!")

if __name__ == "__main__":
    main()
