import cv2
import os
import numpy as np

ASCII_CHARS = '@%#№&()?!/|*+=-;:. '

def resize_image(image, new_width=200):
    width = image.shape[1]
    height = image.shape[0]
    aspect_ratio = height / float(width)
    new_height = int(aspect_ratio * new_width * 0.55)
    return cv2.resize(image, (new_width, new_height))

def pixels_to_ascii(image):
    pixels = image.flatten()
    ascii_str = ''
    for pixel_value in pixels:
        brightness = int(pixel_value / 255 * (len(ASCII_CHARS) - 1))
        ascii_str += ASCII_CHARS[::-1][brightness] 
    return ascii_str

def image_to_ascii(image_path, new_width=200):
    try:
        img = cv2.imread(image_path)
    except Exception as e:
        print(e)
        return

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = resize_image(img, new_width)
    ascii_str = pixels_to_ascii(img)

    img_width = img.shape[1]
    ascii_img = ''
    for i in range(0, len(ascii_str), img_width):
        ascii_img += ascii_str[i:i + img_width] + '\n'

    return ascii_img

def show_images_in_directory(directory):
    files = os.listdir(directory)
    image_files = [file for file in files if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
    print("Фотографии в папке:")
    for idx, image_file in enumerate(image_files):
        print(f"{idx + 1}: {image_file}")

    choice = int(input("Выберите номер фотографии: ")) - 1

    if choice=='exit':
        exit()

    if 0 <= choice < len(image_files):
        return os.path.join(directory, image_files[choice])
    else:
        print("Неверный выбор.")
        return None


def select_directory():
    while True:
        directory = input("Введите путь к директории ('exit' для выхода): ")
        if directory.lower() == 'exit':
            exit()
        if os.path.isdir(directory):
            return directory
        else:
            print("Указанная директория не существует. Пожалуйста, введите корректный путь.")


def create_ascii_file(ascii_image, image_path):
    create_file = input("Хотите сохранить ASCII-арт в файл? (y/n): ")
    if create_file.lower() == 'y':
        output_file = os.path.splitext(image_path)[0] + "_ascii.txt"
        with open(output_file, "w") as file:
            file.write(ascii_image)
            print(f"ASCII-арт сохранен в файл: {output_file}")


def main():
    print("Вы можете выйти из программы в любой момент, написав 'exit'.")
    while True:
        directory = select_directory()
        image_path = show_images_in_directory(directory)
        if image_path:
            ascii_image = image_to_ascii(image_path)
            print(ascii_image)

            create_ascii_file(ascii_image, image_path)

        choice = input("Желаете ли конвертировать еще одно изображение? ('y' для продолжения, 'n' для выхода): ")
        if choice.lower() == 'exit':
            break
        elif choice.lower() == 'n':
            break
        elif choice.lower() != 'y':
            continue


if __name__ == '__main__':
    main()
