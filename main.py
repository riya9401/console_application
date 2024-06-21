from users.client import UserClient
from server.login import Login
from server.user_handler import UserHandler


def main():
    client = UserClient()
    log_in = Login()
    requester = log_in.processLogin()
    user = UserHandler(requester)
    client.close()
    
if __name__ == "__main__":
    main()
