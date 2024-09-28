import PySimpleGUI as sg
import json
import os
import datetime
from PIL import Image, ImageTk

# Function to create a new contentV2.json
def create_contentV2_json(values, image_folder):
    # Force blank if no value is entered
    def force_blank(value):
        return value if value else ""

    # Validate required fields
    def validate_fields(field, name):
        if not field:
            raise ValueError(f"{name} field cannot be blank.")
        if field.endswith(' ,'):
            raise ValueError(f"{name} field cannot end with a space followed by a comma.")
        if field.endswith(','):
            raise ValueError(f"{name} field should not end with a comma.")

    # Validate URL format
    def validate_url(url):
        if url and not url.startswith("https://"):
            raise ValueError("URL must start with 'https://' or be left blank.")

    # Get MIME type based on file extension
    def get_mime_type(filename):
        extension = filename.split('.')[-1].lower()
        return f"image/{extension}"

    try:
        # Validate required fields
        validate_fields(values['artist'], 'Artist')
        validate_fields(values['language'], 'Language')
        validate_fields(values['tags'], 'Tags')
#        validate_fields(values['characters'], 'Characters')

        # Ensure title is filled in
        if not values['title']:
            raise ValueError("Title cannot be blank.")

        # Validate URL
        validate_url(values['url'])

        # Ensure image files folder path is valid
        if not os.path.isdir(image_folder):
            raise ValueError("The image files folder path is invalid.")

        # Filter and count only image files
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
        image_files = [f for f in sorted(os.listdir(image_folder)) if f.lower().endswith(valid_extensions)]
        first_image_path = os.path.join(image_folder, image_files[0]) if image_files else ""

        # Default URL if blank
        url_value = values['url'] if values['url'] else "https://dummyimage.com"

        # Prepare the imageFiles data
        image_files_data = []
        for order, filename in enumerate(image_files, start=1):
            image_file_data = {
                "chapterOrder": -1,
                "favourite": False,
                "isCover": order == 1,  # Page 1 is always the cover
                "isRead": False,
                "isTransformed": False,
                "mimeType": get_mime_type(filename),
                "name": filename.split('.')[0],  # Name without extension
                "order": order,
                "pHash": 0,
                "pageUrl": "",
                "status": "DOWNLOADED",
                "url": f"https://dummyimage.com/{order}"
            }
            image_files_data.append(image_file_data)

        contentV2_data = {
            "attributes": {
                "ARTIST": [{"name": artist.strip().replace(' ', '-'), "type": "ARTIST", "url": f"/artist/{artist.strip().replace(' ', '-').lower()}/"} for artist in force_blank(values['artist']).split(',')],
                "LANGUAGE": [{"name": lang.strip(), "type": "LANGUAGE", "url": f"/language/{lang.strip().lower()}/"} for lang in force_blank(values['language']).split(',')],
                "TAG": [{"name": tag.strip(), "type": "TAG", "url": f"/tag/{tag.replace(' ', '-').lower()}/"} for tag in force_blank(values['tags']).split(',')],
#                "CHARACTER": [{"name": char.strip(), "type": "CHARACTER", "url": f"/character/{char.replace(' ', '-').lower()}/"} for char in force_blank(values['characters']).split(',')],
                "CHARACTER": [],
                "SERIE": [],  # Forced to blank
                "CATEGORY": []  # Forced to blank
            },
            "bookPreferences": {},
            "chapters": [],
            "completed": False,
            "coverImageUrl": "https://dummyimage.com/1",  # Use first image from folder as cover
            "downloadCompletionDate": int(datetime.datetime.now().timestamp() * 1000),
            "downloadDate": int(datetime.datetime.now().timestamp() * 1000),
            "favourite": values['favourite'],  # Checkbox for favorite
            "groups": [],  # Blank
            "imageFiles": image_files_data,  # Processed image files
            "isFrozen": False,  # Forced to blank
            "lastReadDate": 0,  # Forced to blank
            "lastReadPageIndex": 0,  # Default to first page
            "downloadMode": 0,
            "errorRecords": [],
            "manuallyMerged": False,  # Removed and set to False
            "qtyPages": len(image_files),  # Automatically count image files
            "rating": force_blank(values['rating']),
            "reads": 0,  # Default to '0'
            "site": force_blank(values['site']),
            "status": "DOWNLOADED",  # Forced to "DOWNLOADED"
            "title": force_blank(values['title']),
            "uploadDate": int(datetime.datetime.now().timestamp() * 1000),
            "url": url_value  # Use default if blank
        }

        # Write to contentV2.json
        output_file = os.path.join(os.getcwd(), "contentV2.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(contentV2_data, f, indent=4)

        sg.popup('File created!', f'Saved as: {output_file}')
    
    except ValueError as e:
        sg.popup_error(f"Error: {e}")
        return


# Function to update the cover image preview based on the first image in the folder
def update_image_preview(window, image_folder):
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    image_files = [f for f in sorted(os.listdir(image_folder)) if f.lower().endswith(valid_extensions)]
    if image_files:
        first_image_path = os.path.join(image_folder, image_files[0])
        image = Image.open(first_image_path)
        image.thumbnail((200, 200))  # Scale the image down to fit the GUI
        image_tk = ImageTk.PhotoImage(image)
        window['-COVER-IMAGE-'].update(data=image_tk)
        window['qtyPages'].update(len(image_files))  # Update the number of image files
        window.refresh()  # Force GUI to refresh after updating image


# GUI layout
site_list = ["NEXUS", "ANCHIRA", "FAKKU", "EXHENTAI", "ExampleSite"]  # Replace this list with your site options

layout = [
    [sg.Text('Title'), sg.InputText(key='title')],
    [sg.Text('Site'), sg.Combo(site_list, default_value="NEXUS", key='site')],  # Dropdown menu for sites
    [sg.Text('URL'), sg.InputText(key='url')],
    [sg.Text('Completed?'), sg.Checkbox('', key='completed')],
    [sg.Text('Favorite?'), sg.Checkbox('', key='favourite')],  # Favorite checkbox
    [sg.Text('Rating (0-5)'), sg.Slider(range=(0, 5), orientation='h', key='rating')],  # Updated rating range
    [sg.Text('Quantity Pages'), sg.Text('', key='qtyPages')],  # Automatically count and display the number of image files
    
    [sg.Image(key='-COVER-IMAGE-', size=(200, 200))],  # Box for displaying cover image preview
    
    [sg.Text('Artist (comma-separated)'), sg.InputText(key='artist')],
    [sg.Text('Language (comma-separated)'), sg.InputText(key='language')],
    [sg.Text('Tags (comma-separated)'), sg.InputText(key='tags')],
#    [sg.Text('Characters (comma-separated)'), sg.InputText(key='characters')],
    
    [sg.Text('Image Files Folder'), sg.InputText(key='imageFilesFolder', enable_events=True), sg.FolderBrowse(key='folder_browse')],  # Folder for image files
    
    [sg.Button('Create contentV2.json'), sg.Button('Exit')]
]

# Create the window
window = sg.Window('Create contentV2.json', layout, finalize=True)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break  # Exit the loop if the window is closed

    # Handle folder input, whether selected via browse or manually typed
    if event == 'folder_browse' or event == 'imageFilesFolder':
        folder = values['imageFilesFolder']
        if os.path.isdir(folder):  # Ensure folder is valid
            update_image_preview(window, folder)

    if event == 'Create contentV2.json':
        folder = values['imageFilesFolder']
        if os.path.isdir(folder):
            create_contentV2_json(values, folder)  # Create the JSON file
        else:
            sg.popup_error("Please select a valid folder for image files.")

window.close()
