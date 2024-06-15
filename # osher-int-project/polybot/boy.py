import telebot
import cv2
from polybot.img_proc import Img
from dotenv import load_dotenv
import os




load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Check if TELEGRAM_TOKEN is not none
if TELEGRAM_TOKEN is None:
    print("Error: TELEGRAM_TOKEN is not set in the ..env file.")
    exit(1)

# initialize TELEGRAM_BOT
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Dictionary to store the images temporarily
user_images = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Hi there! Send me an image then choose a filter from the following options:\n"
                                      "- Blur\n"
                                      "- Rotate\n"
                                      "- Salt and Pepper\n"
                                      "- Segment\n"
                                      "- convert to grayscale\n"
                                      "- adjust")
# Define a handler for receiving photos
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        print("Received a photo message")
        # Get the photo file ID
        file_id = message.photo[-1].file_id
        # Get the file object using the file ID
        file_info = bot.get_file(file_id)
        # Download the file
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the file temporarily with a unique name based on the file ID
        image_path = f"images/{file_id}.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Check if this is the first image or the second image for concatenation
        if message.chat.id in user_images:
            print("User already has an image in memory")
            if 'concat_pending' in user_images[message.chat.id]:
                print("This is the second image for concatenation")
                # This is the second image for concatenation
                second_image_path = image_path
                first_image_path = user_images[message.chat.id]['concat_pending']
                del user_images[message.chat.id]['concat_pending']  # Remove the pending flag

                # Load the images
                first_image_data = cv2.imread(first_image_path)
                second_image_data = cv2.imread(second_image_path)

                # Concatenate the images
                img_processor = Img(first_image_path)
                concatenated_image = img_processor.concat(second_image_data)
                if concatenated_image is not None:
                    print("Concatenation successful")
                    # Save and send the concatenated image
                    processed_image_path = img_processor.save_image(concatenated_image, suffix='_concatenated')
                    with open(processed_image_path, 'rb') as photo_file:
                        bot.send_photo(message.chat.id, photo_file)
                else:
                    print("Error concatenating images.")
                    bot.reply_to(message, "Error concatenating images.")

                # Clear user
                del user_images[message.chat.id]
            else:
                # This is the first image
                print("This is the first image for concatenation")
                user_images[message.chat.id]['concat_pending'] = image_path
                bot.reply_to(message, "First image saved successfully! Now please send the second image to concatenate with.")
        else:
            # This is the first image+ the choose filter op's
            print("This is the first image received")
            user_images[message.chat.id] = {'concat_pending': image_path}
            bot.reply_to(message, "First image saved successfully! Now to applay concat  filter please send another image or choose a filter from the list \n"
                                      "- Blur\n"
                                      "- Rotate\n"
                                      "- Salt and Pepper\n"
                                      "- Segment\n"
                                      "- convert to grayscale\n"
                                      "- adjust")
    except Exception as e:
        print(f"Error handling image: {e}")
        bot.reply_to(message, f"Error handling image: {e}")
@bot.message_handler(func=lambda message: message.text.lower() in ['blur', 'rotate', 'salt and pepper', 'segment', 'convert to grayscale', 'adjust'])
def handle_filter(message):
    try:
        # Check if the user has previously sent an image
        if message.chat.id in user_images:
            # Get the image path
            if 'concat_pending' in user_images[message.chat.id]:
                image_path = user_images[message.chat.id]['concat_pending']
            else:
                image_path = user_images[message.chat.id]['first_image']

            # Apply the selected filter
            img_processor = Img(image_path)
            filter_name = message.text.lower()
            if filter_name == 'blur':
                processed_image = img_processor.blur()
            elif filter_name == 'rotate':
                processed_image = img_processor.rotate()
            elif filter_name == 'salt and pepper':
                processed_image = img_processor.salt_n_pepper()
            elif filter_name == 'segment':
                processed_image = img_processor.segment()
            elif filter_name == 'convert to grayscale':
                processed_image = img_processor.convert_to_grayscale()
            elif filter_name == 'adjust':
                processed_image = img_processor.adjust_brightness()
            else:
                processed_image = None

            # Check if the filter was applied successfully
            if processed_image is not None:
                # Save and send the processed image
                processed_image_path = img_processor.save_image(processed_image, suffix=f'{filter_name.replace(" ", "")}')
                with open(processed_image_path, 'rb') as photo_file:
                    bot.send_photo(message.chat.id, photo_file)
            else:
                bot.reply_to(message, f"Error applying {filter_name} filter: Result is None.")

            # Remove the image path from the dictionary
            del user_images[message.chat.id]
        else:
            bot.reply_to(message, "Please send an image first.")
    except Exception as e:
        bot.reply_to(message, f"Error processing image: {e}")

# Start your bot with polling +running or not
try:
    print("Bot is running...")
    bot.polling()
except Exception as e:
    print(f"Error starting bot: {e}")



