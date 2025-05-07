from PIL import Image
import time


def local_stretch(input_path, output_path, box, stretch_factor, direction='vertical'):

    # 打开图片并复制副本
    img = Image.open(input_path)
    original = img.copy()
    img.show()
    time.sleep(3)

    # 1. 裁剪选区
    region = original.crop(box)
    region_width, region_height = region.size

    # 2. 计算新尺寸并拉伸局部区域

    new_region_size = (region_width, int(region_height * stretch_factor))

    stretched_region = region.resize(new_region_size)


    # 3. 创建新图层并粘贴拉伸后的区域
    # 计算拉伸后的选区位置（覆盖原区域）
    paste_box = (
            box[0], box[1],
            box[0] + new_region_size[0],
            box[1] + new_region_size[1]
        )

    # 将拉伸区域粘贴到原图
    original.paste(stretched_region, paste_box)

    # 4. 保存结果
    original.save(output_path)
    print("局部拉伸完成！")
    original.show()

    # 使用示例
local_stretch(
            input_path=r"C:\Users\halib\Desktop\nezha2.0.jpg",
            output_path=r"C:\Users\halib\Desktop\nezha3.0.jpg",
            box=(0, 720, 1920, 1440),  # 选区坐标：左，上，右，下
            stretch_factor=1.5,  # 拉伸n倍
            direction='vertical'  # 水平拉伸
        )