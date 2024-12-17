from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
class Fixed_Keyboards:
    """
    Class for defining static Inline and Reply keyboards used throughout the bot.
    """

    @staticmethod
    def init_keyboard():
        """
        Returns the initial keyboard of the bot
        """
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="خرید سلف", callback_data="call_buy_self"),
                InlineKeyboardButton(text="نرخ سلف", callback_data="call_self_price")
            ],
            [InlineKeyboardButton(text=" پشتیبانی", callback_data="call_backup")],
            [
                InlineKeyboardButton(text="سلف چیست؟", callback_data="call_what_self"),
                InlineKeyboardButton(text="راهنمای سلف", callback_data="call_guide")
            ],
            [
                InlineKeyboardButton(text="چک کردن شماره", callback_data="call_check_number"),
                InlineKeyboardButton(text="دریافت API ID", url="https://t.me/get_api_id_hashbot")
            ],
            [InlineKeyboardButton(text="درخواست نمایندگی", callback_data="call_req_agency")],
            [InlineKeyboardButton(text="کانال ما", url="https://t.me/SportBadTweet")],
        ])

    @staticmethod
    def check_keyboard():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="تایید", callback_data="call_confirm_data"),
                InlineKeyboardButton(text="ویرایش", callback_data="call_edit_data")
            ]
        ])

    @staticmethod
    def buy_self_panel():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="درخواست کد", callback_data="call_send_code")],
            [InlineKeyboardButton(text="وارد کردن کد تایید ادمین", callback_data="call_give_admin_code")],
            [InlineKeyboardButton(text="وضعیت درخواست ها", callback_data="call_chcek_buy_self")],
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_home")]
        ])

    @staticmethod
    def back_keyboard():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_home")]
        ])

    @staticmethod
    def admin_connection():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="ارتباط با ادمین", user_id=1463788237)],
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_buy_panel")]
        ])

    @staticmethod
    def create_bot():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="ایجاد ربات", callback_data="call_make_bot")],
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_buy_panel")]
        ])

    @staticmethod
    def for_admins():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="خرید سلف", callback_data="call_buy_self"),
                InlineKeyboardButton(text="نرخ سلف", callback_data="call_self_price")
            ],
            [InlineKeyboardButton(text=" پشتیبانی", callback_data="call_backup")],
            [
                InlineKeyboardButton(text="سلف چیست؟", callback_data="call_what_self"),
                InlineKeyboardButton(text="راهنمای سلف", callback_data="call_guide")
            ],
            [
                InlineKeyboardButton(text="چک کردن شماره", callback_data="call_check_number"),
                InlineKeyboardButton(text="دریافت API ID", url="https://t.me/get_api_id_hashbot")
            ],
            [InlineKeyboardButton(text="کانال ما", url="https://t.me/SportBadTweet")],
            [InlineKeyboardButton(text="درخواست نمایندگی", callback_data="call_req_agency")],
            [InlineKeyboardButton(text='پنل ادمین', callback_data='call_admin_panel')]
        ])

    @staticmethod
    def admins_panel():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="تنظیم متن", callback_data="call_set_texts")],
            [
                InlineKeyboardButton(text="افزودن گیف", callback_data="call_add_gif"),
                InlineKeyboardButton(text="اکانت های موجود", callback_data="call_accounts")
            ],
            [InlineKeyboardButton(text="پیام به تمامی کاربران", callback_data="call_send_to_all")],
            [
                InlineKeyboardButton(text="مدیریت ادمین ها", callback_data="call_handle_admins"),
                InlineKeyboardButton(text="مدیریت بن شدگان", callback_data="call_manage_ban")
            ],
            [InlineKeyboardButton(text="نمایندگی غیرفعال 🔴", callback_data="agency_on")],
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_for_admins")],
        ])

    @staticmethod
    def admin_management():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="ادمین های موجود", callback_data="call_admin_check")],
            [InlineKeyboardButton(text="اضافه کردن ادمین", callback_data="call_add_admin")],
            [InlineKeyboardButton(text="حذف ادمین", callback_data="call_del_admin")],
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_admins_panel")]
        ])

    @staticmethod
    def number_keyboard():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="7️⃣", callback_data="call_number_7"),
                InlineKeyboardButton(text="8️⃣", callback_data="call_number_8"),
                InlineKeyboardButton(text="9️⃣", callback_data="call_number_9")
            ],
            [
                InlineKeyboardButton(text="4️⃣", callback_data="call_number_4"),
                InlineKeyboardButton(text="5️⃣", callback_data="call_number_5"),
                InlineKeyboardButton(text="6️⃣", callback_data="call_number_6")
            ],
            [
                InlineKeyboardButton(text="1️⃣", callback_data="call_number_1"),
                InlineKeyboardButton(text="2️⃣", callback_data="call_number_2"),
                InlineKeyboardButton(text="3️⃣", callback_data="call_number_3")
            ],
            [
                InlineKeyboardButton(text="0️⃣", callback_data="call_number_0"),
                InlineKeyboardButton(text="پاک کردن", callback_data="call_delete_number")
            ],
            [InlineKeyboardButton(text="تایید✅", callback_data="call_confirm_code")]
        ])

    @staticmethod
    def manage_ban():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="اکانت ها", callback_data="call_ban_acocunts")],
            [InlineKeyboardButton(text="شماره تلفن ها", callback_data="call_ban_numbers")],
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_admins_panel")]
        ])

    @staticmethod
    def manage_ban_accounts():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="بن کردن عضو", callback_data="call_ban_member")],
            [InlineKeyboardButton(text="حذف بن", callback_data="call_del_ban_account")],
            [InlineKeyboardButton(text="لیست بن  شدگان", callback_data="call_ban_list_accounts")],
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_manage_ban")]
        ])

    @staticmethod
    def manage_ban_numbers():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="بن کردن شماره تلفن", callback_data="call_ban_number")],
            [InlineKeyboardButton(text="حذف بن", callback_data="call_del_ban_number")],
            [InlineKeyboardButton(text="لیست بن  شدگان", callback_data="call_ban_list_phones")],
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_manage_ban")]
        ])

    @staticmethod
    def back_to_ban_accounts():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_ban_accounts")]
        ])

    @staticmethod
    def back_to_ban_numbers():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_ban_numbers")]
        ])

    @staticmethod
    def share_number_keyboard():
        return ReplyKeyboardMarkup([
            [KeyboardButton("ارسال شماره تلفن من", request_contact=True)]
        ], resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def agency_req():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="ارسال درخواست", callback_data="call_send_req")],
            [InlineKeyboardButton(text="شرایط نمایندگی", callback_data="call_agency_info")],
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_home")]
        ])

    @staticmethod
    def back_to_agency_menu():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_agency_menu")]
        ])

    @staticmethod
    def back_to_set_text():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_set_text")]
        ])

    @staticmethod
    def set_texts():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="تنظیم متن نرخ سلف", callback_data="call_edit_price_self")],
            [InlineKeyboardButton(text="تنظیم متن سلف چیست", callback_data="call_set_wself")],
            [InlineKeyboardButton(text="تنظیم متن راهنما", callback_data="call_set_guide")],
            [InlineKeyboardButton(text="تنظیم متن شرایط نمایندگی", callback_data="call_set_agency_text")],
            [InlineKeyboardButton(text="بازگشت", callback_data="call_back_admins_panel")]
        ])

    @staticmethod
    def buy_cancel_button():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text="لغو ❌", callback_data="call_cancel_buy")]
        ])
        
    @staticmethod 
    def mark():
        return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('🌐𝐺𝑙𝑜𝑏𝑎𝑙 & 𝑃𝑒𝑟𝑠𝑜𝑛𝑎𝑙🦁',callback_data='a')
            ],
            [
                InlineKeyboardButton('𝐴𝑟𝑡𝑖𝑓𝑖𝑐𝑖𝑎𝑙 𝐼𝑛𝑡𝑒𝑙𝑙𝑖𝑔𝑒𝑛𝑐𝑒💭',callback_data='b')
            ],
            [
                InlineKeyboardButton('𝑃𝑟𝑜𝑓𝑖𝑙𝑒🎭',callback_data='c')
            ],
            [
                InlineKeyboardButton('🎮𝐹𝑢𝑛🕹',callback_data='d'),
                InlineKeyboardButton('🤖𝑻𝒂𝒃𝒄𝒉𝒊👾',callback_data='t')
            ],
            [
                InlineKeyboardButton('𝑾𝒆𝒃𝒉𝒐𝒐𝒌🔑',callback_data='q'),
                InlineKeyboardButton('𝑳𝒐𝒄𝒌𝒔🔏',callback_data='s'),
                InlineKeyboardButton('𝑪𝒓𝒐𝒏-𝑱𝒐𝒃🕰',callback_data='r')
            ],
            [
                InlineKeyboardButton('🎨𝑃ℎ𝑜𝑡𝑜 𝐸𝑑𝑖𝑡𝑜𝑟👨‍🎤',callback_data='e'),
                InlineKeyboardButton('🖼𝐿 & 𝐺 𝑀𝑎𝑘𝑒𝑟🧑‍🎤',callback_data='f')
            ],
            [
                InlineKeyboardButton('📸𝑃ℎ𝑜𝑡𝑜 & 𝐺𝑖𝑓📺',callback_data='g'),
                InlineKeyboardButton('🎧𝑀𝑢𝑠𝑖𝑐 & 𝑆𝑡𝑖𝑐𝑘𝑒𝑟🌠',callback_data='h')
            ],
            [
                InlineKeyboardButton('💸𝑀𝑎𝑟𝑘𝑒𝑡🤑',callback_data='i'),
                InlineKeyboardButton('𝐷𝑜𝑤𝑛𝑙𝑜𝑎𝑑𝑒𝑟⬇️',callback_data='j'),
                InlineKeyboardButton('𝑈𝑝𝑙𝑜𝑎𝑑𝑒𝑟⬆️',callback_data='k')
            ],
            [
                InlineKeyboardButton('📖𝐵𝑜𝑜𝑘📚',callback_data='l'),
                InlineKeyboardButton('📝𝑇𝑒𝑥𝑡 𝑀𝑜𝑑𝑒💬',callback_data='m'),
                InlineKeyboardButton('𝐴𝑐𝑡𝑖𝑜𝑛 𝑀𝑜𝑑𝑒💢',callback_data='n')
            ],
            [
                InlineKeyboardButton('𝐴𝑐𝑐𝑜𝑢𝑛𝑡☑️',callback_data='o')
            ],
                    [
                InlineKeyboardButton('𝑇𝑜𝑜𝑙𝑠⚙',callback_data='p')
            ],
            [
                InlineKeyboardButton('𝑪𝒍𝒐𝒔𝒆',callback_data='close')
            ]
        ]
    )

    @staticmethod
    def dast():  
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᗷᗩᑕƘ", callback_data='back')
                ]
            ]
        )

    @staticmethod 
    def openpanelbot():
        return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Panel", switch_inline_query_current_chat='panel')
            ]
        ]
    )


class Dynamic_keyboards:
    """
    Class for defining dynamic keyboards based on user data or other variables.
    """

    @staticmethod
    def create_admin_ids_keyboard(admins, with_id=True):
        buttons = [
            [InlineKeyboardButton(text=f"{admin.admin_user_name} - {admin.admin_id}" if with_id else f"{admin.admin_user_name}", user_id=int(admin.admin_id))]
            for admin in admins
        ]
        buttons.append([InlineKeyboardButton(text="بازگشت", callback_data="call_back_admins_manage")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def create_del_admin_keyboard(admins):
        buttons = [
            [InlineKeyboardButton(text=f"{admin.admin_id}-{admin.admin_user_name}", callback_data=f"call_delete_admin_{admin.admin_id}")]
            for admin in admins
        ]
        buttons.append([InlineKeyboardButton(text="بازگشت", callback_data="call_back_admins_manage")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def create_accounts_keyboard(accounts):
        buttons = [
            [InlineKeyboardButton(text=f"{account.session_name} - {account.phone_number}", callback_data=f"call_account_{account.phone_number}")]
            for account in accounts
        ]
        buttons.append([InlineKeyboardButton(text="بازگشت", callback_data="call_back_admins_panel")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def del_ban_accounts(accounts):
        buttons = [
            [InlineKeyboardButton(text=f"{account}", callback_data=f"call_del_ban_account_{account}")]
            for account in accounts
        ]
        buttons.append([InlineKeyboardButton(text="بازگشت", callback_data="call_back_ban_accounts")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def banned_accounts(accounts):
        buttons = [
            [InlineKeyboardButton(text=f"{account}", user_id=account)]
            for account in accounts
        ]
        buttons.append([InlineKeyboardButton(text="بازگشت", callback_data="call_back_ban_accounts")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def del_ban_numbers(numbers):
        buttons = [
            [InlineKeyboardButton(text=f"{number.phone_number}", callback_data=f"call_del_ban_number_{number.phone_number}")]
            for number in numbers
        ]
        buttons.append([InlineKeyboardButton(text="بازگشت", callback_data="call_back_ban_numbers")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def banned_numbers(numbers):
        buttons = [
            [InlineKeyboardButton(text=f"{number.phone_number}", user_id=number.phone_number)]
            for number in numbers
        ]
        buttons.append([InlineKeyboardButton(text="بازگشت", callback_data="call_back_ban_numbers")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def change_status(keyboard, callback, new_text, new_callback):
        for row in keyboard.inline_keyboard:
            for button in row:
                if button.callback_data == callback:
                    button.text = new_text
                    button.callback_data = new_callback
                    break
        return keyboard
