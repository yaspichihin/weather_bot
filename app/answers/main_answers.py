

def get_new_user_msg(firstname: str) -> str:
    text: str = (
        f"(◕‿◕) Привет {firstname}!\n"
        "Я могу рассказать о текущей погоде!"
    )
    return text


def get_query_msg() -> str:
    text: str = "(＾▽＾) Чем могу помочь?"
    return text
