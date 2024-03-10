import streamlit as st
import os
from PIL import Image
import io
def main():
    st.title("GOES 16 Images")

    folder_path = "/workspaces/goes1/GOES"


    if not os.path.exists(folder_path):
        st.error("Folder not found!")
        return
    folders_with_images = [root for root, _, files in os.walk(folder_path) if any(file.endswith(('.jpg', '.jpeg', '.png', '.gif')) and "" in file for file in files)]
    if len(folders_with_images) == 0:
        st.warning("No folders with images found in the directory!")
        return

    image_types = [["All Images", "Full Color", "Blue", "Red", "Near Infrared", "Cirrus", "Snow/Ice", "Cloud Particle Size", "Thermal", "Upper-level water vapor", "Mid-level water vapor", "Lower-level water vapor", "Cloud-top", "Ozone-level", "Infrared-less sensitive", "Infrared", "Infrared-sensitive", "Carbon Dioxide"],["", "_FC_", "_1_", "_2_", "_3_", "_4_", "_5_", "_6_", "_7_", "_8_", "_9_", "_10_", "_11_", "_12_", "_13_", "_14_", "_15_", "_16_"]]

    folder_selected = st.sidebar.selectbox("Select a folder", folders_with_images)

    present_image_types = []
    file32 = os.listdir(folder_selected)
    for type12 in image_types[1]:
        for file31 in file32:
            if type12 in file31:
                if type12 not in present_image_types:
                    present_image_types.append(type12)
                


    present_image_types_list = [[], present_image_types]
    for img_type24 in present_image_types:
        present_image_types_list[0].append(image_types[0][image_types[1].index(img_type24)])
    
    image_type = st.sidebar.selectbox("Select image type", present_image_types_list[0])
    file_image_type = image_types[1][image_types[0].index(image_type)]
    st.sidebar.write("Timelapse feature is not recommended for all images")
    output_type = st.sidebar.selectbox("Select a display type", ["Timelape", "Images"])
    #date_day = st.sidebar.text_input("Enter the day you want to view (ONLY NUMBER)")
    #date_month = st.sidebar.text_input("Enter the month you want to view (ONLY NUMBER)")
    #date_year = st.sidebar.text_input("Enter the year you want to view (ONLY NUMBER)")

    #full_date = f"_{date_year}{date_month}{date_day}"
    full_date = ""
    
    image_files = [os.path.join(folder_selected, file) for file in os.listdir(folder_selected) if file.endswith(('.jpg', '.jpeg', '.png', '.gif')) and file_image_type in file and full_date in file]

    if len(image_files) == 0:
        st.warning("No images found in the selected folder!")
        return
    
    st.write(folder_selected)
    if output_type == "Timelape":
        
        st.subheader("Timelapse GIF")
        create_timelapse(folder_selected, file_image_type)

    if output_type == "Images":
        
        st.subheader("Images")
        button_key=1
        for img_file in image_files:
            st.image(img_file, use_column_width=True)
            st.text(img_file)
            button_key += 1
            with open(img_file, "rb") as file:
                st.download_button(
                    label="Download",
                    data=file,
                    file_name="image.png",
                    mime="image/png",
                    key=button_key
                    )
            
            
def create_combined_image(folder_path, output_path):
    image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.jpg', '.jpeg', '.png', '.gif')) and "FC" in file]
    if not image_files:
        st.error("No images found in the selected folder!")
        return False

    images = [Image.open(img_file) for img_file in image_files]
    widths, heights = zip(*(img.size for img in images))
    max_width = max(widths)
    total_height = sum(heights)

    combined_image = Image.new("RGB", (max_width, total_height), color=(255, 255, 255))

    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.size[1]

    combined_image.save(output_path)
    return True
    
    
def create_timelapse(folder_path, file_image_type):
    image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.jpg', '.jpeg', '.png', '.gif')) and file_image_type in file]
    image_files.sort(key=os.path.getmtime)
    if len(image_files) == 0:
        st.warning("No image files found in the folder!")
        return
    
    images = [Image.open(img_file).resize((800, 600)) for img_file in image_files]
    gif_bytes = create_gif(images)
    st.image(gif_bytes)
    
    st.download_button(
    label="Download",
    data=gif_bytes,
    file_name="image.gif",
    mime="image/gif"
    )
def create_gif(images):
    gif_bytes = io.BytesIO()
    images[0].save(gif_bytes, format="GIF", save_all=True, append_images=images[1:], loop=0, duration=100)
    return gif_bytes.getvalue()
if __name__ == "__main__":
    main()
