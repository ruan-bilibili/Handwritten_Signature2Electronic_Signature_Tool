import streamlit as st
import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import base64

def convert_signature_to_transparent_png(input_image):
    # 读取图片
    image = np.array(input_image.convert('RGB'))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # 转换到灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 应用二值化处理
    # 使用OTSU自动阈值
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 创建一个RGBA图像（具有透明通道）
    w, h = binary.shape
    transparent_image = Image.new("RGBA", (h, w), (0, 0, 0, 0))
    pixels = transparent_image.load()
    
    # 将二值化图像中的黑色转换为透明，白色转换为黑色
    for i in range(w):
        for j in range(h):
            if binary[i, j] == 255:
                pixels[j, i] = (0, 0, 0, 255)  # 黑色
            else:
                pixels[j, i] = (0, 0, 0, 0)  # 透明
    
    return transparent_image





# 设置配色方案
st.markdown(
    """
    <style>
    .main {
        background-color: ##FFFFFF;
        color: #8E24AA;
    }
    .stButton button {
        background-color: #FF7043;
        color:  #5D4037;
    }
    .stTitle {
        color: #5D4037;
    }
    .stCaption {
        color: #FFAB91;
    }
    </style>
    """,
    unsafe_allow_html=True
)



def main():
    # 侧边栏个人介绍
    st.sidebar.title("关于我")
    #profile_image = Image.open("Image/1.png")  # 替换为你的个人图片路径
    profile_image = Image.open("Image/me2.png")  # 替换为你的个人图片路径
    # 将图像转换为 base64 编码
    buffered = BytesIO()
    profile_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    # 使用st.markdown和HTML/CSS显示图像并使其居中
    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{img_str}" style="width: 150px; border-radius: 50%;">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.write("""
    大家好，我是阮同学，目前在北京师范大学攻读博士。我平时喜欢编程捣鼓一些有趣的玩意儿。如果你有什么新奇的想法或者对我的作品有什么改进建议，欢迎告诉我！\n商务与学习交流：ruan_bilibili@163.com
    """)
    ##滚动字幕
    # 定义滚动字幕的HTML和CSS
    scrolling_text = """
    <div style="overflow: hidden; white-space: nowrap;">
      <div style="display: inline-block; padding-left: 100%; animation: scroll-left 30s linear infinite;font-size: 24px;">
        长期接定制化科研作图，联系方式：ruan_bilibili@163.com。
      </div>
    </div>
    
    <style>
    @keyframes scroll-left {
      0% {
        transform: translateX(0%);
      }
      100% {
        transform: translateX(-100%);
      }
    }
    </style>
    """
    
    # 在Streamlit应用中显示滚动字幕
    st.markdown(scrolling_text, unsafe_allow_html=True)
    st.title("手写签名转换为电子签名工具")
    uploaded_file = st.file_uploader("请选择一张手写签名图片", type=["jpg", "jpeg", "png"], help="支持的文件类型: jpg, jpeg, png. 最大文件大小: 10MB")

    if uploaded_file is not None:
        input_image = Image.open(uploaded_file)
        result_image = convert_signature_to_transparent_png(input_image)
        
        # 显示结果
        st.image(result_image, caption='处理后的签名', use_column_width=True)
        
        # 保存按钮
        buf = BytesIO()
        result_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        if st.download_button(
            label="下载电子签名",
            data=byte_im,
            file_name="电子签名.png",
            mime="image/png"
        ):
            # 下载按钮点击后显示介绍信息和图片
            st.markdown("---")
            money = Image.open("Image/2.jpg")  #
            st.image(money, caption="打赏一下吧！", use_column_width=True)
            st.write("""
            谢谢你使用我的作品！如果觉得好用的话，看在UP这么无私奉献的份上，可否支持下UP呢？我会更加努力做出更好更实用的作品的！
            """)

if __name__ == "__main__":
    main()




    
    
    

#ruan_bilibili@163.com
#https://space.bilibili.com/76702965
#

#python /nfs/home/1002_sunbo/RW_Experiments/Personal_project/Github_Handwritten_Signature2Electronic_Signature_Tool/app.py
