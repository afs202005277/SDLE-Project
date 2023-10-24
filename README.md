# SDLE-Project

General JSON request to server:

- type: AddItem, BoughtItem, CreateList, DeleteList
- token: user's personal token

Extra fields according to type of request:

    AddItem request:
    - name: name of the item
    - quantity: quantity of the item needed
    - listId: id of the list to add the item
    
    BuyItem request:
    - name: name of the item
    - listId: id of the list to add the item
    
    CreateList request:
    - name: name of the list
    - items: json array of Item objects
    
    DeleteList request:
    - id: id of the list




## Team

| Name            | Number    |
| --------------- | --------- |
| Alexandre Nunes | 202005358 |
| André Filipe Sousa     | 202005277 |
| Gonçalo Pinto   | 202004907 |
| Pedro Fonseca   | 202008307 |
