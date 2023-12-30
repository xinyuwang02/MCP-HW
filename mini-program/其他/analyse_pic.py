image_path = r'C:\Users\SF\Desktop\mini-program\其他\image.jpg'

with open(image_path, 'rb') as file:
    byte_count = 0
    while byte_count < 300:
        chunk = file.read(16)
        if not chunk:
            break
        hex_data = ' '.join(f'{byte:02X}' for byte in chunk)
        print(f'{byte_count:04d}: {hex_data}')
        byte_count += 16
