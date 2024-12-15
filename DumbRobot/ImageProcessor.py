from PIL import Image

class ImageProcessor:
    def __init__(self, image_path, max_width, max_height):
        self.image_path = image_path
        self.max_width = max_width
        self.max_height = max_height
        self.pixel_data = self._process_image()

    def _process_image(self):
        # Open the image
        with Image.open(self.image_path) as img:
            # Get current size
            width, height = img.size

            # Determine the final dimensions
            new_width = min(width, self.max_width)
            new_height = min(height, self.max_height)

            # If the image is larger than the given max resolution, resize it
            if width > self.max_width or height > self.max_height:
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                # If smaller, just use the original image as is (cropped to not exceed given max)
                img = img.crop((0, 0, new_width, new_height))

            # Convert image to RGB
            img = img.convert("RGB")

            # Extract pixel data
            pixel_data = []
            for y in range(new_height):
                row = []
                for x in range(new_width):
                    r, g, b = img.getpixel((x, y))
                    row.append((r, g, b))
                pixel_data.append(row)

            return pixel_data

    @staticmethod
    def get_brightness(rgb_tuple):
        r, g, b = rgb_tuple
        return (0.2126*r + 0.7152*g + 0.0722*b) / 256