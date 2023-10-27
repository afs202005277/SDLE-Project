let activeList = null;

function createItem(name, quantity){
    return {
        'name': name,
        'quantity': quantity
    }
}

/**
 * 
 * CLASS SHOPPING LISTS
 * 
 **/

class ShoppingLists{
    constructor(){
        this.lists = this.load();
        this.render();
    }

    load(){
        const list = localStorage.getItem('shoppingLists');
        return list ? JSON.parse(list) : [];
    }

    save(){
        localStorage.setItem('shoppingLists', JSON.stringify(this.lists));
        this.render()
    }

    create(name){
        const existingList = localStorage.getItem(name)
        if(existingList) return

        this.lists.push(name)
        localStorage.setItem(name, [])

        activeList = new ShoppingList(name)
        this.save()
    }

    delete(item, index){
        this.lists.splice(index, 1);
        localStorage.removeItem(item)
        
        if(activeList.getHash() == item)
            activeList = new ShoppingList(this.getFirst())

        this.save()
    }

    render(){
        const ul = document.getElementById('others');
        ul.innerHTML = '';

        this.lists.forEach((item, index) => {
            const cache = localStorage.getItem(item)
            const list = cache !== '' ? JSON.parse(cache) : []
            const quantity = list.reduce((acc,val) => acc + val.quantity, 0)

            const li = document.createElement('li');
            li.classList = 'px-3 w-100 d-flex justify-content-between align-items-center'
            li.innerHTML = `
                <span>${item}</span>
                <div class="d-flex gap-2 align-items-center">
                    <span class="badge bg-primary rounded-pill">${quantity}</span>
                    <i class="fa-solid fa-delete-left"></i>
                </div>
            `
            li.addEventListener('click', () => {
                activeList = new ShoppingList(item)
            });

            li.querySelector('i').addEventListener('click', () => {
                this.delete(item, index);
            });

            ul.appendChild(li);
        });
    }

    getFirst(){
        return this.lists == []
            ? null
            : this.lists[0]
    }
}

const lists = new ShoppingLists()

const addListForm = document.getElementById('addListForm');
addListForm.addEventListener('submit', e => {
    e.preventDefault();

    const input = document.getElementById('list');
    const newList = input.value.trim();
    if(newList !== ''){
        lists.create(newList)
        input.value = ''
    }
});

/**
 * 
 * CLASS SHOPPING LIST
 * 
 **/

class ShoppingList{
    constructor(hash){
        if(hash == null){
            document.querySelector('h3').innerHTML = `You don't have any lists, please create one.`
        } else{
            this.hash = hash
            this.items = this.load();
            this.render();
        }
    }

    getHash(){
        return this.hash
    }

    load(){
        const list = localStorage.getItem(this.hash);
        return list ? JSON.parse(list) : [];
    }

    save() {
        localStorage.setItem(this.hash, JSON.stringify(this.items));
        lists.render()
    }

    modify(func){
        func()
        this.save();
        this.render();
    }

    add(item, quantity) {
        if(this.items.map(i => i.name).includes(item))
            this.modify(() => { 
                this.items.filter(i => i.name == item)[0].quantity += quantity; 
                this.items = this.items.filter(i => i.quantity > 0)
            })
        else if(quantity > 0)
            this.modify(() => { this.items.push(createItem(item, quantity)); })
    }

    delete(index) {
        this.modify(() => { this.items.splice(index, 1); })
    }

    rename(item, newName){
        if(newName == '') return

        if(this.items.map(i => i.name).includes(newName)){
            this.modify(() => { 
                this.items.filter(i => i.name == newName)[0].quantity += item.quantity; 
                this.items = this.items.filter(i => i.name != item.name)
            })
        }
        else
            this.modify(() => { item.name = newName; })
    }

    render() {
        const shoppingList = document.getElementById('shoppingList');
        shoppingList.innerHTML = '';

        document.querySelector('h3').innerHTML = `List: ${this.hash}`

        const deleteModal = document.getElementById('deleteModal')
        const renameModal = document.getElementById('renameModal')

        this.items.forEach((item, index) => {
            const li = document.createElement('li');
            li.classList = 'px-3 w-100 d-flex justify-content-between align-items-center'
            li.innerHTML = `
                <span>${item.name}</span>
                <div class="d-flex gap-2 align-items-center">
                    <span class="badge bg-primary rounded-pill">${item.quantity}</span>
                    <button type="button" class="btn delete" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fa-solid fa-delete-left"></i></button>
                    <button type="button" class="btn rename" data-bs-toggle="modal" data-bs-target="#renameModal"><i class="fa-solid fa-font"></i></button>
                </div>
            `

            li.querySelector('button.delete').addEventListener('click', () => {
                let action = deleteModal.querySelector('.modal-action')
                action.outerHTML = action.outerHTML; // reset listeners
                action = deleteModal.querySelector('.modal-action')
                action.addEventListener('click', () => {
                    this.delete(index);
                })
            })

            li.querySelector('button.rename').addEventListener('click', () => {
                document.getElementById('renameModalLabel').textContent = `Rename item: "${item.name}"`

                let action = renameModal.querySelector('.modal-action')
                action.outerHTML = action.outerHTML; // reset listeners
                action = renameModal.querySelector('.modal-action')
                action.addEventListener('click', () => {
                    this.rename(item, document.getElementById('newName').value)
                })
            })

            shoppingList.appendChild(li);
        });
    }
}

const addItemForm = document.getElementById('addItemForm');
addItemForm.addEventListener('submit', e => {
    e.preventDefault();

    const itemInput = document.getElementById('item');
    const newItem = itemInput.value.trim();

    let quantity = document.getElementById('quantity').value
    if(quantity == '') quantity = 1
    else if(quantity == 0) return
    else quantity = parseInt(quantity)

    if (newItem !== '') {
        activeList.add(newItem, quantity);
        itemInput.value = '';
    }
});


/**
 * 
 * 
 * 
 **/

activeList = new ShoppingList(lists.getFirst())