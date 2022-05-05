from PIL import Image


def merge(img, benefit):
    BOX = (0, 0, 800, 132)

    benefit_area = benefit.crop(BOX)

    w_ratio = img.width / benefit_area.width

    new_height = int(benefit_area.height * w_ratio)

    benefit_area.resize((img.width, new_height))

    result_img = Image.new('RGBA', (img.width, img.height + new_height))
    result_img.paste(benefit_area)
    result_img.paste(img, (0, new_height))
    result_img.save(
        image_path.split('.')[0] + '_benefit.png'
    )


image_path = 'main.jpg'
img1 = Image.open('main.jpg')
img2 = Image.open('additional.png')
merge(img1, img2)
