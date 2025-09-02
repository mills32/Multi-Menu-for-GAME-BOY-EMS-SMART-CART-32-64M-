import os
import array

def main():
    # Initialize variables
    dumb4mo = array.array('B', [255] * (2**22))
    
    # Calculate all possible starting offsets for any rom into the multiboot
    pos32ko = [i * 2**15 + 1 for i in range(1, 128)]
    pos64ko = [i * 2**16 + 1 for i in range(1, 64)]
    pos128ko = [i * 2**17 + 1 for i in range(1, 32)]
    pos256ko = [i * 2**18 + 1 for i in range(1, 16)]
    pos512ko = [i * 2**19 + 1 for i in range(1, 8)]
    pos1024ko = [i * 2**20 + 1 for i in range(1, 4)]
    pos2048ko = [i * 2**21 + 1 for i in range(1, 2)]
    
    # Get list of ROM files
    rom_dir = 'rom'
    listing = []
    for filename in os.listdir(rom_dir):
        if filename.endswith('.gb') or filename.endswith('.gbc'):
            filepath = os.path.join(rom_dir, filename)
            filesize = os.path.getsize(filepath)
            listing.append({'name': filename, 'bytes': filesize})
    
    # Check total size
    total_bytes = sum(item['bytes'] for item in listing)
    if total_bytes > 2**22:
        print('The total size of roms is greater than 4MB!')
        return
    
    # Read MENU ROM
    print('0 = DMG;\n1 = GAME BOY COLOR')
    selected_system = input()
    menu = 0;
    if selected_system == '0':
        menu = 'MottZilla_MenuA.gb'
    if selected_system == '1':
        menu = 'MottZilla_MenuCGBA.gb'
    try:
        with open(menu, 'rb') as f:
            a = array.array('B', f.read())
            # Place the mandatory multiboot rom at the beginning
            for i in range(min(2**15, len(a))):
                dumb4mo[i] = a[i]
    except FileNotFoundError:
        print('mottzilla menu not found!')
        return
    
    # Sort files by size (descending) - bubble sort like in MATLAB code
    n = len(listing)
    for i in range(n):
        for j in range(n - 1):
            if listing[j]['bytes'] < listing[j + 1]['bytes']:
                listing[j], listing[j + 1] = listing[j + 1], listing[j]
    
    games = 0
    
    # Helper function to check if a region is empty (all 255s)
    def is_region_empty(start, size):
        for i in range(size):
            if dumb4mo[start + i] != 255:
                return False
        return True
    
    # Helper function to calculate mean of a region
    def region_mean(start, size):
        total = 0
        for i in range(size):
            total += dumb4mo[start + i]
        return total / size
    
    # Process each ROM file
    for item in listing:
        rom_size = item['bytes']
        
        # 2048KB ROMs
        if rom_size == 2**21:
            if pos2048ko and is_region_empty(pos2048ko[-1] - 1, rom_size):
                fid = os.path.join(rom_dir, item['name'])
                print(f'Slot available for {fid}')
                
                with open(fid, 'rb') as f:
                    a = array.array('B', f.read())
                
                games += 1
                start_idx = pos2048ko[-1] - 1
                for i in range(min(rom_size, len(a))):
                    dumb4mo[start_idx + i] = a[i]
                print('File added to the Multiboot rom')
                
                # Update available positions
                pos1024ko = [p for p in pos1024ko if p < pos2048ko[-1]]
                pos512ko = [p for p in pos512ko if p < pos2048ko[-1]]
                pos256ko = [p for p in pos256ko if p < pos2048ko[-1]]
                pos128ko = [p for p in pos128ko if p < pos2048ko[-1]]
                pos64ko = [p for p in pos64ko if p < pos2048ko[-1]]
                pos32ko = [p for p in pos32ko if p < pos2048ko[-1]]
                
                pos2048ko.pop()
            else:
                print(f'Slot FULL for {item["name"]}: file rejected!')
        
        # 1024KB ROMs
        elif rom_size == 2**20:
            if pos1024ko and is_region_empty(pos1024ko[-1] - 1, rom_size):
                fid = os.path.join(rom_dir, item['name'])
                print(f'Slot available for {fid}')
                
                with open(fid, 'rb') as f:
                    a = array.array('B', f.read())
                
                games += 1
                start_idx = pos1024ko[-1] - 1
                for i in range(min(rom_size, len(a))):
                    dumb4mo[start_idx + i] = a[i]
                print('File added to the Multiboot rom')
                
                # Update available positions
                pos512ko = [p for p in pos512ko if p < pos1024ko[-1]]
                pos256ko = [p for p in pos256ko if p < pos1024ko[-1]]
                pos128ko = [p for p in pos128ko if p < pos1024ko[-1]]
                pos64ko = [p for p in pos64ko if p < pos1024ko[-1]]
                pos32ko = [p for p in pos32ko if p < pos1024ko[-1]]
                
                pos1024ko.pop()
            else:
                print(f'Slot FULL for {item["name"]}: file rejected!')
        
        # 512KB ROMs
        elif rom_size == 2**19:
            if pos512ko and is_region_empty(pos512ko[-1] - 1, rom_size):
                fid = os.path.join(rom_dir, item['name'])
                print(f'Slot available for {fid}')
                
                with open(fid, 'rb') as f:
                    a = array.array('B', f.read())
                
                games += 1
                start_idx = pos512ko[-1] - 1
                for i in range(min(rom_size, len(a))):
                    dumb4mo[start_idx + i] = a[i]
                print('File added to the Multiboot rom')
                
                # Update available positions
                pos256ko = [p for p in pos256ko if p < pos512ko[-1]]
                pos128ko = [p for p in pos128ko if p < pos512ko[-1]]
                pos64ko = [p for p in pos64ko if p < pos512ko[-1]]
                pos32ko = [p for p in pos32ko if p < pos512ko[-1]]
                
                pos512ko.pop()
            else:
                print(f'Slot FULL for {item["name"]}: file rejected!')
        
        # 256KB ROMs
        elif rom_size == 2**18:
            if pos256ko and is_region_empty(pos256ko[-1] - 1, rom_size):
                fid = os.path.join(rom_dir, item['name'])
                print(f'Slot available for {fid}')
                
                with open(fid, 'rb') as f:
                    a = array.array('B', f.read())
                
                games += 1
                start_idx = pos256ko[-1] - 1
                for i in range(min(rom_size, len(a))):
                    dumb4mo[start_idx + i] = a[i]
                print('File added to the Multiboot rom')
                
                # Update available positions
                pos128ko = [p for p in pos128ko if p < pos256ko[-1]]
                pos64ko = [p for p in pos64ko if p < pos256ko[-1]]
                pos32ko = [p for p in pos32ko if p < pos256ko[-1]]
                
                pos256ko.pop()
            else:
                print(f'Slot FULL for {item["name"]}: file rejected!')
        
        # 128KB ROMs
        elif rom_size == 2**17:
            if pos128ko and is_region_empty(pos128ko[-1] - 1, rom_size):
                fid = os.path.join(rom_dir, item['name'])
                print(f'Slot available for {fid}')
                
                with open(fid, 'rb') as f:
                    a = array.array('B', f.read())
                
                games += 1
                start_idx = pos128ko[-1] - 1
                for i in range(min(rom_size, len(a))):
                    dumb4mo[start_idx + i] = a[i]
                print('File added to the Multiboot rom')
                
                # Update available positions
                pos64ko = [p for p in pos64ko if p < pos128ko[-1]]
                pos32ko = [p for p in pos32ko if p < pos128ko[-1]]
                
                pos128ko.pop()
            else:
                print(f'Slot FULL for {item["name"]}: file rejected!')
        
        # 64KB ROMs
        elif rom_size == 2**16:
            if pos64ko and is_region_empty(pos64ko[-1] - 1, rom_size):
                fid = os.path.join(rom_dir, item['name'])
                print(f'Slot available for {fid}')
                
                with open(fid, 'rb') as f:
                    a = array.array('B', f.read())
                
                games += 1
                start_idx = pos64ko[-1] - 1
                for i in range(min(rom_size, len(a))):
                    dumb4mo[start_idx + i] = a[i]
                print('File added to the Multiboot rom')
                
                # Update available positions
                pos32ko = [p for p in pos32ko if p < pos64ko[-1]]
                
                pos64ko.pop()
            else:
                print(f'Slot FULL for {item["name"]}: file rejected!')
        
        # 32KB ROMs
        elif rom_size == 2**15:
            if pos32ko and is_region_empty(pos32ko[-1] - 1, rom_size):
                fid = os.path.join(rom_dir, item['name'])
                print(f'Slot available for {fid}')
                
                with open(fid, 'rb') as f:
                    a = array.array('B', f.read())
                
                games += 1
                start_idx = pos32ko[-1] - 1
                for i in range(min(rom_size, len(a))):
                    dumb4mo[start_idx + i] = a[i]
                print('File added to the Multiboot rom')
                
                pos32ko.pop()
            else:
                print(f'Slot FULL for {item["name"]}: file rejected!')
    
    # Write output file
    if selected_system == '0':
        with open('EMSMULTI.gb', 'wb') as f:
            dumb4mo.tofile(f)
        print('\n\n32M merged DMG rom created, ready to burn!')
    if selected_system == '1':
        with open('EMSMULTI.gbc', 'wb') as f:
            dumb4mo.tofile(f)
        print('\n\n32M merged COLOR rom created, ready to burn!')

if __name__ == '__main__':
    main()