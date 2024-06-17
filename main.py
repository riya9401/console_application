from users.client import UserClient
from server.login import Login
from server.user_handler import UserHandler


def main():
    client = UserClient()
    
    print("1. Login")
    print("2. Exit")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        log_in = Login()
        requester = log_in.processRequest()
        response = client.send_request(f"{requester} loged in succesfully")
        user = UserHandler(requester)
    elif choice == '2':
        print("Exit successfully.")
    client.close()

if __name__ == "__main__":
    main()
