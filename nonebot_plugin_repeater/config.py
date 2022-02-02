from pydantic import Extra, BaseSettings


class Config(BaseSettings):
    test_token: str
    enable_groups: list[int]

    class Config:
        extra = Extra.ignore
        case_sensitive = False