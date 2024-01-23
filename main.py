import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk


def encode_text(image_path, text_to_hide):
    original_image = Image.open(image_path)
    encoded_image = original_image.copy()

    # Convert text to binary
    binary_text = ''.join(format(ord(char), '08b') for char in text_to_hide)

    data_index = 0

    # Iterate over each pixel
    for i in range(encoded_image.width):
        for j in range(encoded_image.height):
            pixel = list(encoded_image.getpixel((i, j)))

            # Encode the text in the least significant bit of each color channel
            for color_channel in range(3):
                if data_index < len(binary_text):
                    pixel[color_channel] = pixel[color_channel] & ~1 | int(binary_text[data_index])
                    data_index += 1

            encoded_image.putpixel((i, j), tuple(pixel))

    encoded_image.save('encoded_image.png')
    return 'Image successfully encoded.'


def decode_text(image_path):
    encoded_image = Image.open(image_path)
    binary_text = ''

    # Iterate over each pixel
    for i in range(encoded_image.width):
        for j in range(encoded_image.height):
            pixel = list(encoded_image.getpixel((i, j)))

            # Extract the least significant bit from each color channel
            for color_channel in range(3):
                binary_text += str(pixel[color_channel] & 1)

    # Convert binary text to ASCII
    decoded_text = ''.join(chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8))
    return decoded_text


class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")

        self.image_path = None

        # UI elements
        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.encode_button = tk.Button(root, text="Encode Text", command=self.encode_text)
        self.encode_button.pack(pady=10)

        self.decode_button = tk.Button(root, text="Decode Text", command=self.decode_text)
        self.decode_button.pack(pady=10)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.show_image()

        print('-----------------')

    def show_image(self):
        img = Image.open(self.image_path)
        img = img.resize((900, 500), Image.ANTIALIAS if 'ANTIALIAS' in dir(Image) else Image.BICUBIC)
        img = ImageTk.PhotoImage(img)

        panel = tk.Label(self.root, image=img)
        panel.image = img
        panel.pack()

        print('-----------------')

    def encode_text(self):
        if self.image_path:
            text_to_hide = input("Enter the text to hide: ")
            result = encode_text(self.image_path, text_to_hide)
            print(result)
        else:
            print("Please upload an image first.")

        print('-----------------')

    def decode_text(image_path):
        try:
            encoded_image = Image.open(image_path)
        except Exception as e:
            return f"Error: {str(e)}"

        binary_text = ''

        # Iterate over each pixel
        for i in range(encoded_image.width):
            for j in range(encoded_image.height):
                pixel = list(encoded_image.getpixel((i, j)))

                # Extract the least significant bit from each color channel
                for color_channel in range(3):
                    binary_text += str(pixel[color_channel] & 1)

        # Convert binary text to ASCII
        decoded_text = ''.join(chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8)).rstrip('\x00')
        print('-----------------')
        return decoded_text


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
